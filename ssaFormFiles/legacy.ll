r1 = call i8* malloc(8)
r1 = bitcast i8* r1, %struct.A*
r2 = 2
r3 = getelementptr %struct.A, %struct.A* r1, 0, 0
store r2, i32* r3
r4 = getelementptr %struct.A, %struct.A* r1, 0, 0
r5 = call i32 @print("%d", r4)
r6 = bitcast %struct.A* r1, i8*
r7 = call i32 @free(r6)