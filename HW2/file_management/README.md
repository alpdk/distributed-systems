# How to use scripts

## How to use *create_user.py* script

This script requires 2 parameters:

1) User name
2) Password

User host address *always (127.0.0.1)* and 
User port address *(more than 5000)* 
generates automatically.


Example of exploitation:

```
create_user.py user_1 abacaba
```

## How to use *delete_user.py* script

This script requires 1 parameters:

1) User name

Example of exploitation:

```
delete_user.py user_1
```

## How to use *add_file.py* script

This script requires 2 parameters:

1) User name
2) File name
3) Local path to the file

Example of exploitation:

```
add_file.py user_1 code_geass_wallpaper /home/alpdk/Pictures/geas.jpg
```

## How to use *delete_file.py* script

This script requires 2 parameters:

1) User name
2) File name

Example of exploitation:

```
delete_file.py user_1 geas.jpg
```

## How to use *getting_specific_user.py* file

This python file contain some small useful methods

If you want to use it, you should import method from this file.

### How to use *get_user_info* method

This method have 1 parameter:

1) User_name *(String format)*

Method return dict if user exist and None if do not.

Example of exploitation:

```
user_info = get_user_info("user_1a")
```

