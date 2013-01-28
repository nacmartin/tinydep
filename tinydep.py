from termcolor import colored
import os

class Deploy:
    commands = []
    rollbackCommands = []
    finishCommands = []
    test = False
    def addCommand(self, command):
        self.commands.append(command)
    def addCommands(self, commands):
        self.commands += commands
    def addRollbackCommand(self, command):
        self.rollbackCommands.append(command)
    def addFinishCommand(self, command):
        self.finishCommands.append(command)
    def processCommand(self, command):
        print colored(command, 'white')
        if not self.test:
            result = os.system(command);
            if result != 0:
                print colored('NOT GOOD', 'red')
                return False
        print colored('OK', 'blue')
        return True
    def processCommands(self):
        for command in self.commands:
            if (isinstance(command, tuple) and len(command) > 1):
                self.addRollbackCommand(command[1])
                if (len(command) > 2):
                    self.addFinishCommand(command[2])
            if isinstance(command, tuple):
                toExecute = command[0]
            else:
                toExecute = command
            if not self.processCommand(toExecute):
                self.rollback()
                return
        self.finish()
    def finish(self):
        print colored(">>>>>>SUCCESS. CLEANING", 'blue')
        for finishCommand in self.finishCommands:
            self.processCommand(finishCommand)
        print colored(">>>>>>HAS GANADO UN VOLVO", 'green')
    def rollback(self):
        print colored(">>>>>>ROLLBACK", 'red')
        for rollbackCommand in self.rollbackCommands:
            self.processCommand(rollbackCommand)

