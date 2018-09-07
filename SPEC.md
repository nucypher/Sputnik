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

### Variables
TODO
