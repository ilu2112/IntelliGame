'''
TODO
dispatch_judge_message:
   * komunikat konca gry
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


    def run(self):
        print "Running SandBox..."
        self.create_threads()
        self.send_initial_data()
        print "Running main loop"
        counter = 1
        while True:
            if self.is_ready_for_read(self.judge_process):
                self.dispatch_judge_message(self.judge_process.stdout.readline())
            if self.is_ready_for_read(self.bot_processes[counter - 1]):
                self.dispatch_bot_message(counter, self.bot_processes[counter - 1].stdout.readline())
            counter = counter + 1
            if counter > self.bot_processes.__len__():
                counter = 1


    def create_threads(self):
        print "Creating programs..."
        # create judge's process
        self.judge_process = Popen(self.judge_exec_command, stdin = PIPE, stdout = PIPE)
        # create bot's processes
        self.bot_processes = []
        for bot_exec_command in self.bots_exec_commands:
            self.bot_processes.append(Popen(bot_exec_command, stdin = PIPE, stdout = PIPE,
                                            preexec_fn = (lambda: set_limits(self.maximum_memory)) ))


    def send_initial_data(self):
        self.judge_process.stdin.write("players: {}\n".format(self.bot_processes.__len__()))
        self.judge_process.stdin.flush()
        self.judge_process.stdin.write("time remaining: {}\n".format(self.maximum_time))
        self.judge_process.stdin.flush()


    def is_ready_for_read(self, process):
        return select.select([process.stdout, ], [], [], 0.0)[0]


    def dispatch_judge_message(self, message):
        if message.__len__() > 0:
            # TODO obsluzyc komunikat konca gry
            bot_number = int(message.split(":")[0].split(" ")[1])
            # TODO obsluzyc wyjatek przerwanego potoku
            self.bot_processes[bot_number - 1].stdin.write(message[message.find(":") + 1:])
            self.bot_processes[bot_number - 1].stdin.flush()


    def dispatch_bot_message(self, bots_number, message):
        if message.__len__() > 0:
            print "   >>> Bot {} message: ".format(bots_number) + str(message)




sb = SandBox("/home/marcin/Desktop/inzynierka/judge",
            ["/home/marcin/Desktop/inzynierka/one_input", "/home/marcin/Desktop/inzynierka/one_input"],
            120)
sb.run()


