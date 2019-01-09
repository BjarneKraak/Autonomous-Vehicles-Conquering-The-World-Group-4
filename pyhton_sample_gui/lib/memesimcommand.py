''' Module for the MemeSimCommand class. '''

class MemeSimCommand(object):

    ''' MemeSimCommand represents a command to be sent to the simulator '''

    CommandList = ['rq', 'mq', 'ip', 'pi', 'tm', 'pc', 'lc', 'ca', 'db']

    def __init__(self, cmdtype, cmdargs):
        if not cmdtype in MemeSimCommand.CommandList:
            raise Exception('Not a valid command type.')
        self._cmdtype = cmdtype
        self._cmdargs = cmdargs

    def asstring(self):
        ''' Return a string for the command to be sent on the TCP connection to the simulator. '''
        # turn all arguments into strings
        strargs = [str(a) for a in self._cmdargs]
        # return the result
        return self._cmdtype+'!'+ '!'.join(strargs)
        
    @staticmethod
    def RQ(team_id, robot_id):
        return MemeSimCommand('rq', [team_id, robot_id])
    
    @staticmethod
    def CA(team_id):
        return MemeSimCommand('ca', [team_id])

    @staticmethod
    def RS(team_id, robot_id, x_pos, y_pos, angle):
        return MemeSimCommand('rs', [team_id, robot_id, x_pos, y_pos,angle])
    
