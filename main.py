"""Module is used to run LifeRecorder class and record some memories."""

from life_recorder.life_recorder import LifeRecorder


def main() -> None:
    """Functions gets the record and writes it to the file."""
    file_name = "life_records.csv"
    one_life = LifeRecorder(file_name)

    # get life record
    life_record = one_life.get_life_record()

    # write life record
    one_life.write_life_record(life_record)

    # read all records
    one_life.read_records(3)


if __name__ == '__main__':
    main()
