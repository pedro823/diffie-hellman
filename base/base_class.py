class BaseClass:
    """ Base class for logging """
    def __init__(min_priority=0, outfile='stdout'):
        self.logger_outfile = outfile
        self.logging_priority = priority
        if self.logger_outfile != 'stdout':
            self.log_file = open(outfile, 'a') # Auto-raises error

    def log(priority, *args):
        if priority >= min_priority:
            msg = ' '.join(args)
            print(msg)
            if self.logger_outfile != 'stdout':
                self.log_file.write(msg + '\n')
