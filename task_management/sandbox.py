'''
TODO
dispatch_judge_message:
   * komunikat przerwanego potoku
ogolnie:
   * licznik czasu
'''

import select

from subprocess import Popen
from subprocess import PIPE
import resource




def set_limits(maximum_memory):
    resource.setrlimit(resource.RLIMIT_AS, (maximum_memory, maximum_memory))




class SandBox():

    def __init__(self, judge_exec_command, bots_exec_commands, maximum_time, maximum_memory):
        self.judge_exec_command = judge_exec_command
        self.bots_exec_commands = bots_exec_commands
        self.maximum_time = maximum_time
        self.maximum_memory = maximum_memory
        self.results = []


    def run(self):
        print "Running SandBox..."
        self.create_threads()
        self.send_initial_data()
        print "Running main loop"
        counter = 0
        while True:
            if self.is_ready_for_read(self.judge_process):
                self.dispatch_judge_message(self.judge_process.stdout.readline())
                if len(self.results) > 0:
                    # kill all and return results
                    for p in self.bot_processes:
                        p.kill()
                    self.judge_process.kill()
                    return self.results
            if self.is_ready_for_read(self.bot_processes[counter]):
                self.dispatch_bot_message(counter, self.bot_processes[counter].stdout.readline())
            counter = counter + 1
            if counter >= self.bot_processes.__len__():
                counter = 0


    def create_threads(self):
        print "Creating programs..."
        # create judge's process
        self.judge_process = Popen(self.judge_exec_command, stdin = PIPE, stdout = PIPE, stderr = None)
        # create bot's processes
        self.bot_processes = []
        for bot_exec_command in self.bots_exec_commands:
            self.bot_processes.append(Popen(bot_exec_command, stdin = PIPE, stdout = PIPE, stderr = None,
                                            preexec_fn = (lambda: set_limits(256 * 1024 * 1024)) ))


    def send_initial_data(self):
        self.judge_process.stdin.write("players: {}\n".format(self.bot_processes.__len__()))
        self.judge_process.stdin.flush()
        self.judge_process.stdin.write("time remaining: {}\n".format(self.maximum_time))
        self.judge_process.stdin.flush()


    def is_ready_for_read(self, process):
        return select.select([process.stdout, ], [], [], 0.0)[0]


    def dispatch_judge_message(self, message):
        if message.__len__() > 0:
            if message.find("results begin") > -1:
                # end game
                while not self.is_ready_for_read(self.judge_process):
                    line = ""
                line = self.judge_process.stdout.readline()
                while line.find("results end") == -1:
                    self.results.append((int(line.split(" ")[0]), line.split(" ")[1].strip()))
                    while not self.is_ready_for_read(self.judge_process):
                        line = ""
                    line = self.judge_process.stdout.readline()
                try:
                    self.judge_process.stdin.write("exit\n")
                    self.judge_process.stdin.flush()
                except IOError:
                    pass
            else:
                # message for a bot
                bot_number = int(message.split(":")[0].split(" ")[1])
                try:
                    self.bot_processes[bot_number - 1].stdin.write(message[message.find(":") + 1:])
                    self.bot_processes[bot_number - 1].stdin.flush()
                except IOError:
                    pass


    def dispatch_bot_message(self, bots_number, message):
        if message.__len__() > 0:
            try:
                self.judge_process.stdin.write("bot " + str(bots_number) + ": " + message)
                self.judge_process.stdin.flush()
            except IOError:
                pass



sb = SandBox("java -cp /home/marcin/Pulpit/inz/ AverageTheGame".split(" "),
            ["python /home/marcin/Pulpit/inz/AlwaysFive.py".split(" "), "python /home/marcin/Pulpit/inz/AlwaysThirty.py".split(" ")],
            120,
            256)
print(str(sb.run()))