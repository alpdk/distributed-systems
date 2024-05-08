# How to use scipts

## How t use *create_user.py* srcipt

This script requires 4 parameters:

1) User name
2) Password
3) User host address *(192.168.0.1 - 192.168.255.254)*
4) User port address *(more than 5000)*

Example of exploitation:

```
create_user.py user_1 abacaba 192.168.0.1 5000
```

## How t use *delete_user.py* srcipt

This script requires 1 parameters:

1) User name

Example of exploitation:

```
delete_user.py user_1
```

## How t use *add_file.py* script

This script requires 2 parameters:

1) User name
2) Local path to the file

Example of exploitation:

```
add_file.py user_1 /home/alpdk/Pictures/geas.jpg
```

## How t use *delete_file.py* script

This script requires 2 parameters:

1) User name
2) File name

Example of exploitation:

```
delete_file.py user_1 geas.jpg
```