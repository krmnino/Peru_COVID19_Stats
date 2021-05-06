from matplotlib.figure import Figure
import warnings
import sys

warnings.filterwarnings('ignore')

class QuadPlot:
    def __init__(self, colors_sp, titles_sp, enable_rolling_avg_sp, type_sp, x_label_sp, y_label_sp, x_data, y_data, spt):        
        if(len(colors_sp) != 4):
            sys.exit('num_sublots does not equal colors_sp')
        else:
            self.colors_subplots = colors_sp
        
        if(len(titles_sp) != 4):
            sys.exit('num_sublots does not equal titles_sp')
        else:
            self.titles_subplots = titles_sp

        if(len(enable_rolling_avg_sp) != 4):
            sys.exit('num_sublots does not equal enable_rolling_avg_sp')
        else:
            self.enable_rolling_avg_subplots = enable_rolling_avg_sp

        if(len(type_sp) != 4):
            sys.exit('num_sublots does not equal type_sp')
        else:
            self.type_subplots = type_sp

        if(len(x_label_sp) != 4):
            sys.exit('num_sublots does not equal x_label_sp')
        else:
            self.x_label_subplots = x_label_sp

        if(len(y_label_sp) != 4):
            sys.exit('num_sublots does not equal y_label_sp')
        else:
            self.y_label_subplots = y_label_sp

        if(len(x_data) != 4):
            sys.exit('num_sublots does not equal x_data')
        else:
            self.x_data = x_data

        if(len(y_data) != 4):
            sys.exit('num_sublots does not equal y_data')
        else:
            self.y_data = y_data

        self.suptitle = spt
        self.text_font = {'fontname':'Bahnschrift'}
        self.digit_font = {'fontname':'Consolas'}

        self.fig = Figure(figsize=(14, 10), dpi=200)

        self.axes = [self.fig.add_subplot(2,2,1),
                     self.fig.add_subplot(2,2,2),
                     self.fig.add_subplot(2,2,3),
                     self.fig.add_subplot(2,2,4)]

        self.fig.subplots_adjust(left=0.05, bottom=0.10, right=0.98, top=0.94, wspace=0.15, hspace=0.38)
        for i in range(0, 4):
            if(self.type_subplots[i] == 'bar'):
                self.bar_plot(i)
            elif(self.type_subplots[i] == 'scatter'):
                self.scatter_plot(i)
        
        self.fig.suptitle(self.suptitle, fontsize=10)
        self.fig.savefig('test.png')

    def bar_plot(self, index):
        
        self.axes[index].grid(zorder=0)
        self.axes[index].bar(self.x_data[index], self.y_data[index], color=self.colors_subplots[index], zorder=2)
        self.axes[index].set_title(self.titles_subplots[index], **self.text_font)
        self.axes[index].tick_params(axis='x',labelrotation=90)
        self.axes[index].set_xticklabels(labels=self.x_data[index], fontsize=8, **self.digit_font)
        for tick in self.axes[index].get_yticklabels():
            tick.set_fontname(**self.digit_font)
        self.axes[index].set_xlabel(self.x_label_subplots[index], **self.text_font)
        self.axes[index].set_ylabel(self.y_label_subplots[index], **self.text_font)

    def scatter_plot(self, index):
        self.axes[index].plot(self.x_data[index], self.y_data[index], color=self.colors_subplots[index])
        self.axes[index].plot(self.x_data[index], self.y_data[index], 'ko')
        self.axes[index].set_title(self.titles_subplots[index])
        self.axes[index].tick_params(axis='x',labelrotation=90)
        self.axes[index].set_xticklabels(labels=self.x_data[index], fontsize=8, **self.digit_font)
        for tick in self.axes[index].get_yticklabels():
            tick.set_fontname(**self.digit_font)
        self.axes[index].set_xlabel(self.x_label_subplots[index], **self.text_font)
        self.axes[index].set_ylabel(self.y_label_subplots[index], **self.text_font)
        self.axes[index].grid()
        