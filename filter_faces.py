import argparse
import filter
import recognize

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add_faces", help="Folder that is the name of the person containing their pictures")
    parser.add_argument("-r", "--recognize", action="store_true", help="Start video recognition from known_faces")
    parser.add_argument("-i", "--interval", type=int, help="Frame count to process")
    args = parser.parse_args()

    if args.add_faces:
        filter.filter_dir(args.add_faces)
    elif args.recognize:
        recognize.recognize(args.interval)



