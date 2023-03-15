from qiskit import *
from qiskit.providers.ibmq.job import *
from qiskit.tools.visualization import *
import matplotlib.pyplot as plt

def show(fig):
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)
    plt.show()

def adder(n1) : 
    n1 = [str(n) for n in n1] #stringify the numbers
    l = len(max(n1, key=len)) #take longest string
    n1 = [n.zfill(l)[::-1] for n in n1] #pad with zero and reverse
    dvc = 'statevector_simulator'
    qr = QuantumRegister(4) #regsiter 4 quantum (a,b,Ci,Co)
    cr = ClassicalRegister(l+1) #length + 1 regisster to store result
    qc = QuantumCircuit(qr, cr) # create ciscuit
    for i in range(0, l): #loop through l
        qc.reset(qr) #reset all to avoid interference from perv result
        if(n1[0][i] == '1'): qc.x(0) # set 1 if number has 1 
        if(n1[1][i] == '1'): qc.x(1) # set 1 if number has 1 
        qc.x(qr[2]).c_if(l,1) # set 1 if last cl register has value 1,i.e., set Ci=1 if prev Co =1 
        qc.ccx(0,1,3) #apply toffoli gate
        qc.cx(0,1) #apply cnot gate
        qc.ccx(1,2,3) #apply toffoli 
        qc.cx(1,2) #apply cnot
        qc.cx(0,1) #apply cnot (not required for half adder)
        qc.measure(qr[2],cr[i]) # measure sum to ClRegister
        qc.measure(qr[3],cr[l]) # measure Co to last ClRegister

    be = Aer.get_backend(dvc) #get backend
    jb = execute(qc, backend=be, shots=100) #run 100 slots
    if(dvc != 'statevector_simulator'): 
        job_monitor(jb)
    jres_counts = jb.result().get_counts() 
    return {'r':jres_counts, 'c':qc.draw('mpl'), 'h':plot_histogram(jres_counts)}
    
res = adder([11100,100101])
print(res) 
show(res['h'])
show(res['c'])
