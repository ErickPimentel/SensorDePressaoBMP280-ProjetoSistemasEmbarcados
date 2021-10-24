import time

class LcdApi: 
    LCD_MOVE_DISP       = 0x08  
    LCD_MOVE_RIGHT      = 0x04   
    LCD_CGRAM           = 0x40  
    LCD_DDRAM           = 0x80  
    LCD_RS_CMD          = 0
    LCD_RS_DATA         = 1
    LCD_RW_WRITE        = 0
    LCD_RW_READ         = 1
    LCD_MOVE            = 0x10  
    LCD_CLR             = 0x01  
    LCD_HOME            = 0x02  
    LCD_ENTRY_MODE      = 0x04  
    LCD_ENTRY_INC       = 0x02  
    LCD_ENTRY_SHIFT     = 0x01  
    LCD_ON_CTRL         = 0x08  
    LCD_ON_DISPLAY      = 0x04  
    LCD_ON_CURSOR       = 0x02  
    LCD_ON_BLINK        = 0x01  
    LCD_FUNCTION        = 0x20  
    LCD_FUNCTION_8BIT   = 0x10  
    LCD_FUNCTION_2LINES = 0x08  
    LCD_FUNCTION_10DOTS = 0x04  
    LCD_FUNCTION_RESET  = 0x30

    def __init__(self, value_ln, value_clms):
        self.value_ln = value_ln
        if self.value_ln > 4:
            self.value_ln = 4
        self.value_clms = value_clms
        if self.value_clms > 40:
            self.value_clms = 40
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.backlight = True
        self.vanish()
        self.display_off()
        self.no_cursor()
        self.display_on()
        self.backlight_on()
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)

    def display_on(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def display_off(self):
        self.hal_write_command(self.LCD_ON_CTRL)

    def backlight_on(self):
        self.backlight = True
        self.hal_backlight_on()

    def backlight_off(self):
        self.backlight = False
        self.hal_backlight_off()

    def skip_info(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3f
        if cursor_y & 1:
            addr += 0x40    
        if cursor_y & 2:    
            addr += self.value_clms
        self.hal_write_command(self.LCD_DDRAM | addr)

    def no_cursor(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def blink_cursor_off(self):
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY |
                               self.LCD_ON_CURSOR)

    def putchar(self, char):
        if char == '\n':
            if self.implied_newline:
                
                
                pass
            else:
                self.cursor_x = self.value_clms
        else:
            self.hal_write_data(ord(char))
            self.cursor_x += 1
        if self.cursor_x >= self.value_clms:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = (char != '\n')
        if self.cursor_y >= self.value_ln:
            self.cursor_y = 0
        self.skip_info(self.cursor_x, self.cursor_y)

    def putstr(self, string):
        for char in string:
            self.putchar(char)

    def hal_backlight_on(self):
        pass

    def hal_backlight_off(self):
        pass

    def hal_write_command(self, cmd):
        raise NotImplementedError

    def hal_write_data(self, data):
        raise NotImplementedError

    def vanish(self):
        
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0