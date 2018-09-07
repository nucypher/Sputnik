# Sputnik Specification

#### WARNING: This is hackathon code! It's not meant to be used in production for anything. It's really bad and it's not really a language. This is just a proof of concept -- like a rapid prototype. The author has no experience implementing compilers or interpreters.

### Format
Sputnik looks/feels like an assembly level language. Since FHE is built out of logic gates, it made
sense to me (tux) to build something that looks like it could be compiled and executed in a VM. Maybe this helps us prototype and reason about future applications for Fully Homomorphic Encryption.

The following is the format:

```
[OPCODE] <arguments>
```

## OPCODES
### Program Entrance/Exit

All Sputnik programs begin with an entrance OPCODE and end with an exit OPCODE:
```
BOOTSTRAP <inputs>
...
EXIT
```
When `BOOTSTRAP` is called, the Sputnik execution engine expects the first unnamed
parameter to be a bootstrapping key that the program can use to operate on ciphertext.

The following inputs are entrance inputs to the Sputnik program:
```
BOOTSTRAP plain pad
```
In the above example, the variables `plain` and `pad` are encrypted inputs to
the Sputnik program.

To declare the end of the Sputnik program and return the encrypted state, simply
call `EXIT`:
```
BOOTSTRAP plain pad
...
EXIT
```

### Variables

Fully Homomorphic programs must be executed linearly. Branching makes programs
complex and hard to control and reason with. For a general rule, it appears that
branching is easier if you do it very early on during execution so you can use
multiplexing to get the program back into an easier-to-control linear state.

We can declare an encrypted variable by pushing the state or an input. It can be
read as, "PUSH var into new_var". Continuing from our above example:
```
...
PUSH plain STATE
```
TODO

### Comments

Sputnik doesn't have inline comments, but you can write a comment via the semi-colon:
```
...
; Copy the state
PUSH STATE my_state
```
