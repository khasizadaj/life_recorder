# Life Recorder

A CLI based approach to save records. Records can be categorized with tags.

> Records are saved locally in the specified directory by user. JSON file format is used to save records.

[TOC]

## Usage

```shell
# run as python script
$ py .\main.py <command> <identifier>

# run as an .exe file
$ life_recorder <command> <identifier>
```

### Commands

- `create`
- `read`
- `read <identifier>`
- `update <identifier>`
- `delete <identifier>`

#### create

This command adds a new record to the database.

User needs to provide these inputs to create new record:

- `<tag>` (optional)
- `<title`
- `<content>`

```shell
$ py .\main.py create

  # user inputs
  What is the tag of record (optional)?: <tag>
  What is the title of record? <title>
  What is the content of this record? <content>

  # output
  Record added successfully:

  id: <identifier>
  timestamp: <timestamp>
  tag: <tag>
  title: <title>
  content: <content>
```

> `<identifier>` and `<timestamp>` are generated by program automatically.

#### read

This command can be used with or without providing an identifier. If it is without any identifier, it will read and print all existing records in the database.

```shell
$ py .\main.py read

  # output
  id: <identifier>
  timestamp: <timestamp>
  tag: <tag>
  title: <title>
  content: <content>

  id: <identifier>
  timestamp: <timestamp>
  tag: <tag>
  title: <title>
  content: <content>

  ...

```

However, if user provides an identifier for command, it will read and print record that has specified identifier in the database.

```shell
$ py .\main.py read <correct_identifier>

  # output
  id: <correct_identifier>
  timestamp: <timestamp>
  tag: <tag>
  title: <title>
  content: <content>

```

#### update

This command always requires an identifier to perform the operation. It takes an identifier and prints record for user to remind what was the record; then asks to update any fields that can be updated, i.e. title, tag, content.

```shell
$ py .\main.py update <identifier>

  # reminder
  Current record:

  id: <identifier>
  timestamp: <timestamp>
  tag: <tag>
  title: <title>
  content: <content>

  Usage: Add new detail for respective field. If you want to keep any value untouched, press "Enter".

  # user inputs
  What is the updated tag? (optional): <new_tag>
  What is the updated title?: <new_title>
  What is the updated content?: <new_content>

  # output
  Record with #1 is updated.

```

> User can keep any field as it is by providing no new detail and pressing `Enter`. This information is displayed for user as well.

#### delete

This command always requires an identifier to perform the operation. It takes an identifier and prints record for user to remind what is the record; then it asks the user to confirm deletion of record. If user confirms, it will delete it.

```shell
$ py .\main.py update <identifier>

  Record you want to delete is:
  id: <identifier>
  timestamp: <timestamp>
  tag: <tag>
  title: <title>
  content: <content>

  Are you sure you want to delete this record? [Y(y) / N(n)]:

  # user confirms deletion by writing "y" or "Y"
  Deleting record ... Don't stop adding new records!

  Successfully deleted record.

  # user aborts deletion by writing "n" or "N"
  Every record matters! I am glad that you didn't delete it!

```

### using .exe file

**TBA**
