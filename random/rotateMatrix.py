import numpy as np


def general_rotateMatrix90deg(Sqmatrix):
    """
    Given an n x n 2D matrix, rotate the image by 90 degrees (clockwise).

    """

    n = len(Sqmatrix)
    newmatrix = np.zeros((n, n))

    if n == 2:
        for i in range(n):
            for j in range(n):

                if i == 0 and j == n - 1:
                    newmatrix[i, j] = Sqmatrix[0, 0]

                elif i == n - 1 and j == 0:
                    newmatrix[i, j] = Sqmatrix[n - 1, n - 1]

                elif i == n - 1 and j == n - 1:
                    newmatrix[i, j] = Sqmatrix[0, n - 1]

                elif i == 0 and j == 0:
                    newmatrix[i, j] = Sqmatrix[n - 1, 0]

    elif n > 2:
        newmatrix[0, :] = Sqmatrix[:, 0][::-1]
        newmatrix[:, n - 1] = Sqmatrix[0, :]

        newmatrix[n - 1, :] = Sqmatrix[:, n - 1][::-1]
        newmatrix[:, 0] = Sqmatrix[n - 1, :]

        # change the center piece
        newmatrix[(n - 1) / 2, (n - 1) / 2] = Sqmatrix[(n - 1) / 2, (n - 1) / 2]

        tmp = Sqmatrix[1:n - 1, 1:n - 1]
        new_n = len(Sqmatrix)

        call_times = np.floor((n - 2) / 2)
        # print call_times
        count = 0

        while count < call_times:
            new_n = n
            # print newmatrix
            newmatrix[1:new_n - 1, 1:new_n - 1] = general_rotateMatrix90deg(tmp)
            # print newmatrix
            new_n = len(newmatrix[1:new_n - 1, 1:new_n - 1])
            # import pdb; pdb.set_trace()
            # print new_n
            count += 1
    return newmatrix


blah = np.arange(4).reshape(2, 2) + 1
print general_rotateMatrix90deg(blah)

blah = np.arange(9).reshape(3, 3) + 1
print general_rotateMatrix90deg(blah)

blah = np.arange(16).reshape(4, 4) + 1
print general_rotateMatrix90deg(blah)

blah = np.arange(25).reshape(5, 5) + 1
print general_rotateMatrix90deg(blah)

blah = np.arange(36).reshape(6, 6) + 1
print general_rotateMatrix90deg(blah)

blah = np.arange(49).reshape(7, 7) + 1
print general_rotateMatrix90deg(blah)
