# Simple s-expression interpreter

### Preprocessor Directives:

#### Includes:

Include the entirety of another file in place of the line
`#inc file.txt`.
This line will be replaced with the contents of file.txt

#### Macros:

Substitute one string for another. If
`#def test (print 'this will print test')`
is in a program, every spot after that that has the word test (not in a string)
will be replaced with the print expression

### Built-in functions:

Name        | Action                                                          | Example
------------|-----------------------------------------------------------------|-------------------------
print       | Print to the terminal                                           | `(print 'Hello World!')`
assign      | Assign to a variable                                            | `(assign x 5)`
add\_assign | Add to a variable and assign its result                         | `(add_assign x 5)`
sub\_assign | Sub from a variable and assign its result                       | `(sub_assign x 5)`
mul\_assign | Mul to a variable and assign its result                         | `(mul_assign x 5)`
div\_assign | Div with a variable and assign its result                       | `(div_assign x 5)`
mod\_assign | Mod with a variable and assign its result                       | `(mod_assign x 5)`
neg         | Negate one number                                               | `(neg 5)`
add         | Add two numbers                                                 | `(add 1 2)`
sub         | Subtract two numbers                                            | `(sub 5 4)`
mul         | Multiply two numbers                                            | `(mul 2 2)`
div         | Divide two numbers                                              | `(div 9 3)`
mod         | Get the remainder from dividing                                 | `(mod 9 3)`
eq          | Return true if two items are equal                              | `(eq 9 3)`
gt          | Return true if the first is greater than the second             | `(dlt 9 3)`
lt          | Return true if the first is less than the second                | `(gt 9 3)`
ge          | Return true if the first is greater than or equal to the second | `(ge 9 3)`
le          | Return true if the first is less than or equal to the second    | `(le 9 3)`
if          | Conditionally do something                                      | `(if (> x 0)(print x))` or `(if (> x 0) x 0)`
nop         | Do nothing, use to chain                                        | `(nop (print 'two!') (print 'expressions!'))`
lst         | Form all arguments into a list                                  | `(lst 1 2 3 4 5)`
append      | Append an item to the end of a list                             | `(= x (lst 1 2 3)) (append x 4)`
