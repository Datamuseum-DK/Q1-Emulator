

from multiprocessing import shared_memory
# Attach to the existing shared memory block

shm = shared_memory.SharedMemory(name='shm_q1', create=False)


a = [f'{x:02x}' for x in shm.buf[:512]]
print(' '.join(a))
