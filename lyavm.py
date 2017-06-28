class LyaVM():

    def interpret(self, prog, heap=[]):
        #program memory
        P = prog
        #stack memory
        M = [0]*100000
        #display
        D = [0]*100
        #heap for string constants
        H = heap
        #program counter and stack pointer
        pc = 0 
        sp = 0
        #print(P, M, D, H, pc, sp) 
        #Generate jumps with correct program Counter
        labels = {}
        for i in range(0,len(P)):
            if P[i][0] == "lbl":
                labels[P[i][1]] = i
        for i in range(0,len(P)):
            if P[i][0] == "jmp" or P[i][0] == "jof":
                P[i] = (P[i][0], labels[P[i][1]])
        #Keep interpreting while instruction is not 'end'
        while (P[pc][0] != 'end'):
            print(P, P[pc], pc);
            if (P[pc][0] == 'ldc'):
                sp = sp + 1
                M[sp] = P[pc][1]
            elif (P[pc][0] == 'ldv'):
                sp = sp + 1
                M[sp] = M[D[P[pc][1]]+P[pc][2]]
            elif (P[pc][0] == 'ldr'):
                sp = sp + 1
                M[sp] = D[P[pc][1]] + P[pc][2]
            elif (P[pc][0] == 'stv'):
                M[D[P[pc][1]] + P[pc][2]] = M[sp]
                sp = sp - 1
            elif (P[pc][0] == 'lrv'):
                sp = sp + 1
                M[sp]=M[M[D[P[pc][1]] + P[pc][2]]]
            elif (P[pc][0] == 'srv'):
                M[M[D[P[pc][1]]+P[pc][2]]] = M[sp]
                sp = sp - 1
            elif (P[pc][0] == 'add'):
                M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
            elif (P[pc][0] == 'sub'):                  
                M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
            elif (P[pc][0] == 'mul'):
                M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
            elif (P[pc][0] == 'div'): 
                M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
            elif (P[pc][0] == 'mod'):
                M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
            elif (P[pc][0] == 'neg'):
                M[sp]= -M[sp]

            elif (P[pc][0] == 'abs'):
                M[sp]= abs(M[sp])
            elif (P[pc][0] == 'and'): 
                M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
            elif (P[pc][0] == 'lor'):
                M[sp-1]=M[sp-1] or M[sp];  sp=sp-1
            elif (P[pc][0] == 'not'):
                M[sp]= not M[sp]
            elif (P[pc][0] == 'les'):
                M[sp-1]=M[sp-1] = M[sp];  sp=sp-1
            elif (P[pc][0] == 'leq'):
                M[sp-1]=M[sp-1] <= M[sp];  sp=sp-1
            elif (P[pc][0] == 'grt'):
                M[sp-1]=M[sp-1] > M[sp];  sp=sp-1
            elif (P[pc][0] == 'gre'):
                M[sp-1]=M[sp-1] >= M[sp];  sp=sp-1
            elif (P[pc][0] == 'equ'):
                M[sp-1]=M[sp-1] == M[sp];  sp=sp-1
            elif (P[pc][0] == 'neq'):
                M[sp-1]=M[sp-1] != M[sp];  sp=sp-1
            elif (P[pc][0] == 'jmp'):
                pc=P[pc][1]
                continue
            elif (P[pc][0] == 'jof'):
                if not M[sp]:
                    pc=P[pc][1]
                else:
                    pc=pc+1
                    sp=sp-1
                continue
            elif (P[pc][0] == 'alc'):
                sp=sp+P[pc][1]
            elif (P[pc][0] == 'dcl'):
                sp=sp-P[pc][1]
            elif (P[pc][0] == 'cfu'):
                sp=sp+1; M[sp]=pc+1; pc=P[pc][1]; continue
            elif (P[pc][0] == 'enf'):
                sp=sp+1; M[sp]=D[P[pc][1]]; D[P[pc][1]]=sp+1
            elif (P[pc][0] == 'ret'):
                D[P[pc][1]]=M[sp]; pc=M[sp-1]; sp=sp-(P[pc][2]+2); continue
            elif (P[pc][0] == 'idx'):
                M[sp-1]=M[sp-1] + M[sp] * P[pc][1]
                sp=sp-1
            elif (P[pc][0] == 'grc'):
                M[sp]=M[M[sp]]
            elif (P[pc][0] == 'lmv'):
                t=M[sp]
                M[sp:sp+P[pc][1]]=M[t:t+P[pc][1]]
                sp += (P[pc][1]-1)
            elif (P[pc][0] == 'smv'):
                t = M[sp-P[pc][1]]
                M[t:t+P[pc][1]] = M[sp-P[pc][1]+1:sp+1]
                sp -= (P[pc][1]+1)
            elif (P[pc][0] == 'smr'):
                t1 = M[sp-1]
                t2 = M[sp]
                M[t1:t1+P[pc][1]] = M[t2:t2+P[pc][1]]
                sp -= 1
            elif (P[pc][0] == 'sts'):
                adr=M[sp]
                M[adr]=len(H[P[pc][1]])
                for c in H[P[pc][1]]:
                    adr=adr+1
                    M[adr]=c;
                sp=sp-1
            elif (P[pc][0] == 'rdv'):
                sp=sp+1;  M[sp]=input()
                try:
                    M[sp] = int(M[sp])
                except:
                    M[sp] = M[sp]
            elif (P[pc][0] == 'rds'):
                strg=input()
                adr=M[sp]
                M[adr] = len(strg)
                for k in strg:
                    adr=adr+1
                    M[adr]=k
                sp=sp-1
            elif (P[pc][0] == 'prv'):
                if P[pc][1]:
                    print(chr(M[sp]))
                else:
                    print(M[sp]);
                sp=sp-1
            elif (P[pc][0] == 'prt'):
                print(M[sp-P[pc][1]+1:sp+1]);
                sp-=(P[pc][1]-1)
            elif (P[pc][0] == 'prc'):
                print(H[P[pc][1]],end="")
            elif (P[pc][0] == 'prs'):
                adr = M[sp]
                leng = M[adr]
                for i in range(0,leng):
                    adr = adr + 1
                    print(M[adr],end="")
                    sp=sp-1
            elif (P[pc][0] == 'stp'):
                sp = -1
                D[0] = 0
            
            #increase program counter 
            pc = pc + 1


            print(P, P[pc], pc);
