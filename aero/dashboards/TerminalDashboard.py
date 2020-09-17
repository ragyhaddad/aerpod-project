# Author: Ragy Haddad
import curses 
from aero.enums import JobStatus 
from aero.loggers import ProgressLogger 

class TerminalDashboard:
    def __init__(self):
        self.logger = ProgressLogger()
        self.begin_x = 0; self.begin_y = 0
        self.height = 300; self.width = 300
    # Contrust a depth tree
    def dep_tree(self,workflow):
        level_tree = {}
        max_x = 1
        is_dependant_on = []
        max_name_len = [len(j) for j in list(workflow.keys())]
        max_name_len = max(max_name_len)
        indent = max_name_len + 1
        for job_name_i in workflow["jobs"].keys(): 
            j_ = workflow["jobs"][job_name_i]
            if len(j_["depends_on"]) == 0:
                max_x = 1 
                level_tree[job_name_i] = max_x
            for job_name_j in workflow["jobs"]:
                curr_job = workflow["jobs"][job_name_j]
                if job_name_i in curr_job["depends_on"]:
                    level_tree[job_name_j] = level_tree[job_name_i] + indent 
                    max_x = max_x + indent
        return level_tree
    # Stream Progress
    def stream_progress(self,pipeline_name):
        if self.logger.check_pipeline_exists(pipeline_name) == False:
            exit(1)
        scr = curses.initscr()
        scr.scrollok(True)
        scr.keypad(1)
        curses.halfdelay(5) 
        curses.start_color()      
        curses.noecho()
        # Colors 
        curses.init_color(10, 100,100,100) 
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)       
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # Update 
        self.update_screen(scr,pipeline_name)
    # Format output
    def update_screen(self,scr,pipeline_name):
        padding = 1
        cur_pos = -1
        num_rows, num_cols = scr.getmaxyx()
        pad = curses.newpad(2000, 2000)
        pad.keypad(1)
        pad.bkgd(' ',curses.color_pair(10))
        # Initial Current State
        current_state = self.logger.get_current_state(pipeline_name)
        # Headers
        scr.addstr(0,0,"PIPELINE: %s" % pipeline_name,curses.A_BOLD)
        scr.addstr(0,30,"last updated: %s" % current_state["last_updated"],curses.A_BOLD)
        scr.refresh()
        while True:
            scroll_init = False
            current_state = self.logger.get_current_state(pipeline_name)
            try:
                c = pad.getch() 
                if c == 3:
                    curses.endwin()
                    exit(0)
                if c == ord("q"):
                    curses.endwin()
                    exit(0)
                if c == curses.KEY_DOWN:
                    cur_pos += 1
                    pad.refresh(cur_pos,0,1,0,num_rows - 1,num_cols - 1)
                    scroll_init = True
                    continue
                if c == curses.KEY_UP:
                    cur_pos -= 1
                    pad.refresh(cur_pos,0,1,0,num_rows - 1,num_cols - 1)
                    scroll_init = True
                    continue
                pad.erase()
                scr.addstr(0,30,"last updated: %s" % current_state["last_updated"],curses.A_BOLD)
                scr.refresh()
                if scroll_init == False:
                    self.format_output(current_state,pad,num_rows,num_cols,cur_pos)
            except KeyboardInterrupt:
                curses.endwin()
                exit(0)
            
    # Write outputs
    def format_output(self,current_state,pad,num_rows,num_cols,cur_pos):
        cur_pos = 0
        workflow_name = list(current_state["workflows"].keys())[0]
        workflow = current_state["workflows"][workflow_name]
        n_lines = len(list(workflow["jobs"].keys()))
        depth_tree = self.dep_tree(workflow) 
        for idx,job_name in enumerate(workflow["jobs"].keys()):
            job = workflow["jobs"][job_name]
            status = job["status"]
            dependencies = job["depends_on"]
            x_depth = depth_tree[job_name]
            pad.addstr(idx,0,job_name,curses.COLOR_WHITE)
            pad.addstr(idx,30,"▇",curses.color_pair(status + 1))
            pad.addstr(idx,34,JobStatus(status).name)
            if len(dependencies) > 0 and status == JobStatus.QUEUED.value:
                pad.addstr(idx,45,"Awaiting Dep Jobs")
        pad.clrtoeol()
        pad.refresh(cur_pos,0,1,0,num_rows - 1,num_cols - 1)
        curses.napms(1000)
        

if __name__ == "__main__":
    pass

    


            

                

            


