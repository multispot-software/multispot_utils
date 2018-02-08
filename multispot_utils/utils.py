from pathlib import Path
import pandas as pd
from IPython.display import HTML

pd.options.display.max_columns = 48
pd.options.display.max_rows = 48


def info_html(d):
    """Fancy HTML display of FRETBursts's Data information in the Notebook.
    """
    fname = Path(d.fname)
    laser_powers = d.setup['excitation_input_powers'] * 1e3
    power_unit = 'mW'
    if any(laser_powers[laser_powers > 0] < 10):
        power_unit = 'μW'
        laser_powers *= 1e3
    laser_wavelengths = d.setup['excitation_wavelengths'] * 1e9
    span = "<span style='display: inline-block; width: {size}px;'> {text} </span>"
    s = f"""
    <h3>{span.format(text='File:', size=100)} {fname.name}</h3>
    <h3>{span.format(text='Folder:', size=100)} {fname.parent}</h3>
    <blockquote><p class="lead">{d.description.decode()}</p></blockquote>
    <ul>
    <li>{span.format(text='Measurement Type:', size=150)} {d.meas_type} &nbsp;&nbsp;&nbsp; ({d.nch} spot)</li>
    <li>{span.format(text='Acquisition duration:', size=150)} {float(d.acquisition_duration):.1f} s </li>
    <li>{span.format(text='Laser power:', size=150)}
    """
    for wavelen, power in zip(laser_wavelengths, laser_powers):
        s += f'<b>{power:.0f} {power_unit}</b> @ {wavelen} nm &nbsp;&nbsp;&nbsp;'
    s += '</li>'
    if d.alternated:
        s += f"<li>{span.format(text='ALEX period [offset]:', size=150)} "
        s += f"{d.alex_period} ({d.alex_period*d.clk_p*1e6:.1f} μs) [{d.offset}]</li>"
    s += '</ul>'
    return HTML(s)


def _make_df_bursts(list_of_columns):

    ncols = 48
    assert len(list_of_columns) == ncols
    nrows = max(len(x) for x in list_of_columns)
    columns = np.arange(ncols)
    df = pd.DataFrame(columns=columns, index=np.arange(nrows), dtype=float)
    df.columns.name = 'spot'
    for col, col_data in zip(columns, list_of_columns):
        df.iloc[:len(col_data), col] = col_data
    return df


def _make_df_spots(list_of_tuples=None):
    nrows = 48
    df = pd.DataFrame(index=np.arange(nrows))
    if list_of_tuples is None:
        list_of_tuples = []
    for col, col_data in list_of_tuples:
        df[col] = col_data
    return df


def cal_phrate(d, stream, phrates=None, recompute=False):
    Path('results').mkdir(exist_ok=True)
    if phrates is None:
        phrates = {}
    phrates_fname = Path('results/%s_phrate_%s.csv' % (mlabel, stream))
    phrates_fnameB = Path('results/%s_phrate_%sB.csv' % (mlabel, stream))
    if phrates_fname.is_file() and not recompute:
        phrates[str(stream)] = pd.read_csv(phrates_fname, index_col=0)
        phrates[str(stream)].index.name = 'spot'
        phr = pd.read_csv(phrates_fnameB, index_col=0)
        phr.columns = [int(c) for c in phr.columns]
        phr.columns.name = 'spot'
        phrates[str(stream) + 'B'] = phr
    else:
        try:
            d.calc_max_rate(m=10, ph_sel=stream, compact=True)
        except ValueError:
            d.calc_max_rate(m=10, ph_sel=stream, compact=False)
        phrates[str(stream) + 'B'] = _make_df_bursts(d.max_rate)
        phrates[str(stream)] = (
            _make_df_spots()
            .assign(**{'num_bursts': d.num_bursts})
            .assign(**{'num_nans': [np.isnan(x).sum() for x in d.max_rate]})
            .assign(**{'num_valid': lambda x: x.num_bursts - x.num_nans})
            .assign(**{'valid_fraction': lambda x: 100 * x.num_valid / x.num_bursts})
        )
        phrates[str(stream)].to_csv(phrates_fname)
        phrates[str(stream) + 'B'].to_csv(phrates_fnameB)

    print('   Valid fraction (mean of all ch): %.1f %%' %
          phrates[str(stream)].valid_fraction.mean())
    return phrates
