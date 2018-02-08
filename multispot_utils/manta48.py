from collections import defaultdict
import numpy as np


# Spot with horizontal layout
# first row goes from 0 to 11 (left to right)
spotsh = np.arange(48).reshape(4, 12)

# Spots with vertical layout
# The top left corner (0, 0) is 47, columns decrease as row increases
spotsv = spotsh.T[::-1, ::-1]

pixel_block = {
    'center': spotsv[4:8],
    'top': spotsv[:4],
    'bottom': spotsv[-4:]}

block_map = {i: v for i, v in enumerate(
                ['bottom' if pixel in pixel_block['bottom']
                 else 'center' if pixel in pixel_block['center']
                 else 'top'
                 for pixel in range(48)])
            }


def get_binmap(bin_row=2, bin_col=2, spots=spotsv):
    """Get the (row, col) bin coordinate for each pixel.
    """
    shape = (spots.shape[0] // bin_row,
             spots.shape[1] // bin_col,
             bin_row * bin_col)
    binned_spots = np.zeros(shape, dtype='int8')
    for row in range(bin_row):
        for col in range(bin_col):
            binned_spots[:, :, col + bin_row * row] = \
                spots[row::bin_row, col::bin_col]

    bin_map = [tuple(int(i) for i in np.where(binned_spots == pixel)[:2])
               for pixel in range(48)]
    return {i: v for i, v in enumerate(bin_map)}


bin2x2_map = {k: str(v)
              for k, v in get_binmap(2, 2, spots=spotsv).items()}

bin2x2_invmap = defaultdict(list)
for spot, bin2x2 in bin2x2_map.items():
    bin2x2_invmap[bin2x2].append(spot)

bin4x4_map = get_binmap(4, 4)

block_coord_to_name = {
    (0, 0): 'top',
    (1, 0): 'center',
    (2, 0): 'bottom',
}
bin4x4_name = {k: block_coord_to_name[v] for k, v in bin4x4_map.items()}

assert block_map == bin4x4_name
