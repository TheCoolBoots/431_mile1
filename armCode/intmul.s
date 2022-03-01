
.arch armv7-a
.global intmul

intmul:
    push {v1, v2, v3, v4, lr}
    @Initializing values
    mov v1, #32
    mov v2, #0
    mov v3, a1
    mov v4, a2

    @ v1 = N,  v2 = A, v3 = X = B, v4 = Y = Q
    @ performs A <- X * Y

loop:
    @checking if the right most bit of y is 1
    and a3, v4, #1
    cmp a3, #1
    @branches and skips the add if not 1
    bne continue
    @moving values into registers for function int add
    mov a1, v2
    mov a2, v3
    bl intadd
    mov v2, a1

continue:
    @Shifting values of x and y
    lsl v3, v3, #1
    lsr v4, v4, #1
    @moving values into registers to call int add
    mov a1, v1
    mov a2, #-1
    bl intadd
    mov v1, a1
    
    @Checking if n is = to 0
    cmp v1, #0
    @Branches to loop if n is not 0
    bne loop
    mov a1, v2
    
    @restore registers
    pop {v1, v2, v3, v4, pc}
    


