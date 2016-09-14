
import osnap.osnapy
import osnap.util


def create_osnapy(verbose):

    # we currently have slightly different versions across the OSs
    if osnap.util.is_windows():
        python_version = '3.5.2'
    elif osnap.util.is_mac():
        python_version = '3.5'
    else:
        raise NotImplementedError

    osnap.osnapy.make_osnapy(python_version, verbose=verbose)


if __name__ == '__main__':
    create_osnapy(True)
