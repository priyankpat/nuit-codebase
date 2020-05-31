from threading import Thread


class File:
    def __init__(self):
        self.reg_file = './data/reg.txt'

    def read(self):
        list = []
        with open(self.reg_file, 'r') as filehandle:
            for f in filehandle:
                list.append(f.replace('\n', ''))
        print(list)
        return list

    def empty(self):
        self.write([])

    def write(self, data):
        def write_job():
            file = open(self.reg_file, 'w')
            for d in data:
                file.write(d + '\n')
            file.close()

        write_thread = Thread(target=write_job, args=())
        write_thread.daemon = True
        write_thread.start()

    def remove(self, key):
        def remove_job():
            l = self.read()
            if key in l:
                l.remove(key)
                self.write(l)

        remove_thread = Thread(target=remove_job, args=())
        remove_thread.daemon = True
        remove_thread.start()

    def add(self, key):
        def add_job():
            l = self.read()
            if key not in l:
                l.append(key)
                self.write(l)

        add_thread = Thread(target=add_job, args=())
        add_thread.daemon = True
        add_thread.start()
