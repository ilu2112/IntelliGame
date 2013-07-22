class SandBox():

    def __init__(self, judge_exec_command, bots_exec_commands, maximum_time, maximum_memory):
        self.bots_exec_commands = bots_exec_commands


    def run(self):
        results = []
        for _ in range(0, self.bots_exec_commands.__len__()):
            results.append((0, '---'))
        results[-1] = (1, '---');
        return results