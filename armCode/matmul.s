////////////////////////////////////////////////////////////////////////////////
// You're implementing the following function in ARM Assembly
//! C = A * B
//! @param C          result matrix
//! @param A          matrix A 
//! @param B          matrix B
//! @param hA         height of matrix A
//! @param wB         width of matrix B
//
//void matmul(int* C, const int* A, const int* B, unsigned int hA, unsigned int wA, unsigned int wB)
//{
//  for (unsigned int i = 0; i < hA; ++i)
//    for (unsigned int j = 0; j < wB; ++j) {
//      int sum = 0;
//      for (unsigned int k = 0; k < wA; ++k) {
//        sum += A[i * wA + k] * B[j * wB + k];
//      }
//      C[i * wB + j] = sum;
//    }
//}
////////////////////////////////////////////////////////////////////////////////

.arch armv7-a
    .text
.global matmul
    .align  1
    .syntax unified

matmul:
@Saving values to the stack
push {v1,v2,v3,v4,v5,v6,v7,lr}
mov v1, a4

@grabbing the extra arguements
ldr v2, [sp, #32]
ldr v3, [sp, #36]
@loading addresses to save for the following loop

@C is at sp + 8
@A is at sp + 4
@B is at sp + 0
push {a1}
push {a2}
push {a3}

@ldr a1, [sp, #4]
@cmp a1, v7
@bne notE
@mov a1, #4
@b ending
@notE:
@mov a1, #2
@ending:


@reset values to 0
mov v4, #0
mov v5, #0
mov v6, #0
mov v7, #0



@ v1 = hA, v2 = wA, v3 = wB, v4 = i, v5 = j, v6 = k, v7 = sum

for1:
    @checking to see to exit the loop
    cmp v4, v1
    bge end1
    for2:
        @checking to exit the second loop
        cmp v5, v3 
        bge end2
        mov v7, #0
        for3:
            @checking to exit the third loop
            cmp v6, v2
            bge end3
            @ sum += A[4(i * wA + k)] * B[4(j * wB + k)];
            
            @ a1 <- 4(i * wA + k)   
            
            mov a1, v4
            mov a2, v2
            bl intmul
            mov a2, v6
            bl intadd
            mov a2, #4
            bl intmul
            @ a3 <- A + 4(i * wA + k)
            ldr a2, [sp, #4]                @ a2 <- A
            bl intadd
            push {a1}
            
            @ a1 <- 4(j * wB + k)
            mov a1, v5
            mov a2, v3
            bl intmul
            mov a2, v6
            bl intadd
            mov a2, #4
            bl intmul
            @ a1 < B + 4(j * wB + k)
            ldr a2, [sp, #4]                @ a2 <- B
            bl intadd
            
            @ a1 <- *(A + 4(i * wA + k)) * *(B + 4(j * wB + k))
            pop {a2}
            ldr a2, [a2]
            ldr a1, [a1]        @ a1 <- *(B + 4(j * wB + k))
            bl intmul
            

            @ sum += ...
            mov a2, v7
            bl intadd
            mov v7, a1
            
                
            

            @ increment k
            mov a1, v6
            mov a2, #1
            bl intadd
            mov v6, a1
            b for3
        end3:
        @ reset k to 0
        mov v6, #0
        
        @ v1 = hA, v2 = wA, v3 = wB, v4 = i, v5 = j, v6 = k, v7 = sum
        
        @ C[4(i * wB + j)] = sum;
        
        @ a1 <- 4(i * wB + j)
        mov a1, v4
        mov a2, v3
        bl intmul
        mov a2, v5
        bl intadd
        mov a2, #4
        bl intmul

        ldr a2, [sp, #8]            @ a2 <- C
        bl intadd               @ a1 <- a1 + a2
        str v7, [a1]            @ C[4(i * wB + j)] <- sum

        @ increment j
        mov a1, v5
        mov a2, #1
        bl intadd
        mov v5, a1
        b for2
    end2:
    @ reset j to 0
    mov v5, #0
    
    @ increment i
    mov a1, v4
    mov a2, #1
    bl intadd
    mov v4, a1
    b for1
end1:
    @ restore registers
    pop {a2,a3,a4,v1,v2,v3,v4,v5,v6,v7,lr}
    bx lr


