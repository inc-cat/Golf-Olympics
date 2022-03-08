import csv
from matplotlib import pyplot
from fpdf import FPDF
import os


# adding optional extras to fpdf library
class PDF(FPDF):
    def header(self):
        self.set_font('courier', 'B', 25)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        # self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)

        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('courier', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, '-' + str(self.page_no()) + '-', 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('courier', '', 12)
        # Background color
        self.set_fill_color(127, 100, 255)
        # Title
        self.cell(0, 6, 'Part %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text fileOT
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        self.set_font('courier', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)


    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)


# stats read from csv file
with open('stats.csv') as csv_file:
    game_data = list(csv.reader(csv_file))


# par, and both participation stats are split into 3 lists
par = list(map(int, game_data[0]))
me = list(map(int, game_data[1]))
friend = list(map(int, game_data[2]))
cat = list(map(int, game_data[3]))

total_shots = len(par)

# these lists will be for the combined score of every hole taken
continued_par = []
me_total = []
friend_total = []
cat_total = []

for ascending in range(1, total_shots + 1):
    continued_par.append(sum(par[0:ascending]))
    me_total.append(sum(me[0:ascending]))
    friend_total.append(sum(friend[0:ascending]))
    cat_total.append(sum(cat[0:ascending]))

# these lists will be for the result against par on every hole taken
me_result = []
friend_result = []
cat_result = []
hole_index = 0

# taking the par amount away from the total shots taken to get score result
for par_descent in par:
    me_result.append(me[hole_index]- par_descent)
    friend_result.append(friend[hole_index] - par_descent)
    cat_result.append(cat[hole_index] - par_descent)
    hole_index +=1

me_raverage = []
friend_raverage = []
cat_raverage = []
for get_av in range(total_shots + 1):
    if get_av == 0:
        continue
    me_sum = sum(me_result[0:get_av])
    me_raverage.append(me_sum / (get_av))
    friend_sum = sum(friend_result[0:get_av])
    friend_raverage.append(friend_sum / get_av)
    cat_sum = sum(cat_result[0:get_av])
    cat_raverage.append(cat_sum / get_av)



# plotting first graph for shots against par cumilatively
x_axis = [i for i in range(total_shots)]
pyplot.figure(figsize=(10, 5), dpi=150)
pyplot.xlabel('Hole')
pyplot.ylabel('Score')
pyplot.axvline(x=18, ymin=0, ymax=1, color='000000')
pyplot.axvline(x=36, ymin=0, ymax=1, color='000000')
pyplot.axvline(x=54, ymin=0, ymax=1, color='000000')
pyplot.axvline(x=72, ymin=0, ymax=1, color='000000')
pyplot.axvline(x=90, ymin=0, ymax=1, color='000000')
pyplot.plot(x_axis, continued_par, color='#000000', linestyle='dashed',
    label='Par')
pyplot.plot(x_axis, me_total, color='#800000',#marker = 'x',
    label='Anwar')
pyplot.plot(x_axis, friend_total, color='#FF0000',#marker = 'x',
    label='Todd')
pyplot.plot(x_axis, cat_total, color='#35a3fc',#marker = 'x',
    label='Adam')

pyplot.title('Golf scores')
pyplot.legend()
pyplot.savefig('graph1.png')
pyplot.close()

# offsetting the x coordinates by 0.2 each way to have bars centred
# the combined offset is the same as the width of the bars.
x1 = []
x2 = []
for x in x_axis:
    x1.append(x + 0.2)
    x2.append(x - 0.2)

# plotting second graph for shots agsinst part individually
pyplot.figure(figsize=(11, 8), dpi=150)
pyplot.xlabel('Hole')
pyplot.ylabel('difference')
pyplot.plot(x_axis, [0] * total_shots, color='#000000', label='Par')
pyplot.bar(x2, me_result, color='#d99898', width=0.27,
    label='Anwar')
pyplot.bar(x1, friend_result, color='#ff7070', width=0.27,
    label='Todd')
pyplot.bar(x_axis, cat_result, color='#97ff82', width=0.27,
    label='Adam')
pyplot.plot(x_axis, me_raverage, color='#400b0b', linestyle='dashed',
    label='Anwar average result')
pyplot.plot(x_axis, friend_raverage, color='#801d1d', linestyle='dashed',
    label='Todd average result')
pyplot.plot(x_axis, cat_raverage, color='#4e614a', linestyle='dashed',
    label='Adam average result')

pyplot.title('Golf scores')
pyplot.legend()
pyplot.savefig('graph2.png')
pyplot.close()


# showing all hole in notable results
# hole in 1, ablatross, eagle, birdie, par, bogey, double bogey, forfeit
me_uo = [0, 0]
friend_uo = [0, 0]
cat_uo = [0, 0]
for under_over in range(total_shots):
    if me_result[under_over] < 0:
        me_uo[0] +=1
    elif me_result[under_over] > 0:
        me_uo[1] +=1
    if friend_result[under_over] < 0:
        friend_uo[0] +=1
    elif friend_result[under_over] > 0:
        friend_uo[1] +=1
    if cat_result[under_over] < 0:
        cat_uo[0] +=1
    elif cat_result[under_over] > 0:
        cat_uo[1] +=1

# some unused statistics pulled from results to be potentially used later
me_hi1 = me.count(1)
me_alb = me_result.count(-3)
me_eag = me_result.count(-2)
me_bir = me_result.count(-1)
me_par = me_result.count(0)
me_bog = me_result.count(1)
me_dob = me_result.count(2)
me_forfeit = me.count(19)
friend_hi1 = friend.count(1)
friend_alb = friend_result.count(-3)
friend_eag = friend_result.count(-2)
friend_bir = friend_result.count(-1)
friend_par = friend_result.count(0)
friend_bog = friend_result.count(1)
friend_dob = friend_result.count(2)
friend_forfeit = friend.count(19)
cat_hi1 = me.count(1)
cat_alb = me_result.count(-3)
cat_eag = me_result.count(-2)
cat_bir = me_result.count(-1)
cat_par = me_result.count(0)
cat_bog = me_result.count(1)
cat_dob = me_result.count(2)
cat_forfeit = me.count(19)


# bar chart for under over stats
# the list below is the values that will replace numbers in the graph
score_tiers = ['Under par', 'Par', 'Over Par']
# the bar width is cut to 0.27 to have all 3 bars lines, to offset bat posotion
bar_width = 0.27
y_pos = [0, 1, 2]

pyplot.figure(figsize=(10, 5), dpi=150)
pyplot.xticks(y_pos, score_tiers)
pyplot.bar(y_pos, [me_uo[0], me_par, me_uo[1]],
    width=bar_width, label='Anwar')
pyplot.bar(y_pos,[me_hi1, 0, 0], width=bar_width,
    label='- Hole in one')
pyplot.bar([0.27, 1.27, 2.27], [friend_uo[0], friend_par,
    friend_uo[1]], width=bar_width, label='Todd')
pyplot.bar([0.27, 1.27, 2.27], [friend_hi1, 0, 0],
    width=bar_width, label='- Hole in one')
pyplot.bar([0.54, 1.54, 2.54], [cat_uo[0], cat_par,
    cat_uo[1]], width=bar_width, label='Adam')
pyplot.bar([0.54, 1.54, 2.54], [cat_hi1, 0, 0],
    width=bar_width, label='- Hole in one')
pyplot.legend()

pyplot.savefig('graph3.png')
pyplot.close()


WIDTH = 210
HEIGHT = 297

# Title for pdf
title = 'Golf With Your Friends'


# create pdf with parameters
pdf = PDF('P', 'mm', (210, 297))
pdf.set_title(title)
pdf.set_author('Anwar Louis')
# pdf.add_page()
# pdf.set_font('courier', 'U', 20)
# pdf.cell(0, 10, 'Golf With Your Friends.', ln=True)
pdf.print_chapter(1, 'Introduction', 'init_text.txt')

pdf.set_font('courier', 'U', 14)
pdf.cell(0, 2, '', ln=True)
pdf.cell(0, 5, 'Gamplay stats', ln=True)

# plotting results table
# each course is 18 holes so values can be split in lots of 18
total_games = int(total_shots / 18)
start = [i for i in range(0, total_shots, 18)]
end = [i for i in range(18, total_shots + 1, 18)]
# each course name is at the start of every 18 cells
# all names are extracted
courses = list(filter(('').__ne__, game_data[4]))
cols = ['Par', 'Anwar', 'Todd', 'Adam']

game_coord = []
for plot_game in range(total_games):
    game_coord.append([start[plot_game], end[plot_game]])

# formatting and plotting table using a for loop
for plot_table in range(total_games):
    pdf.set_font('courier', '', 12)

    # print(courses[plot_table])

    pdf.cell(0, 5,'Course' + str(plot_table + 1) + ': ' +
        courses[plot_table], ln=True)


    st_pos = game_coord[plot_table][0]
    en_pos = game_coord[plot_table][1]
    par_show = ['Par'] + list(map(str, par[st_pos:en_pos]))
    Anwar_show = ['Anwar'] + list(map(str, me[st_pos:en_pos]))
    friend_show = ['Todd'] + list(map(str, friend[st_pos:en_pos]))
    cat_show = ['Adam'] + list(map(str, cat[st_pos:en_pos]))



    pdf.set_font("courier", size=8)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 19  # distribute content evenly
    pdf.cell(0, 10, '', ln=True)

    for row in [par_show, Anwar_show, friend_show, cat_show]:
        for datum in row:
            pdf.multi_cell(col_width, line_height,
                datum, border=1, ln=3, max_line_height=pdf.font_size)
        pdf.ln(line_height)

    pdf.cell(0, 5,'' , ln=True)
    pdf.cell(0, 5,'Total par:' + str(sum(par[st_pos:en_pos])), ln=True)
    pdf.cell(0, 5,'Anwar total:' + str(sum(me[st_pos:en_pos])), ln=True)
    pdf.cell(0, 5,'Todd total:' + str(sum(friend[st_pos:en_pos])), ln=True)
    pdf.cell(0, 5,'Adam total:' + str(sum(cat[st_pos:en_pos])), ln=True)

# stats used for page 2 analysis
par_total = sum(par)
me_total = sum(me)
me_final =  me_total - par_total
friend_total = sum(friend)
friend_final = friend_total - par_total
cat_total = sum(cat)
cat_final = cat_total - par_total

pdf.cell(0, 5,'' , ln=True)
pdf.set_font('courier', 'U', 15)
pdf.cell(0, 5,'Standings:' + str(par_total), ln=True)
pdf.set_font('courier', '', 8)
pdf.cell(0, 5,'Final Par:' + str(par_total), ln=True)
pdf.cell(0, 5,'Anwar:' + str(me_total) + ' (' + str(me_final) + ')', ln=True)
pdf.cell(0, 5,'Todd:' + str(friend_total) +
    ' (' + str(friend_final) + ')', ln=True)
pdf.cell(0, 5,'Anwar:' + str(cat_total) + ' (' + str(cat_final) + ')', ln=True)

# graph for bottom of page 1
pdf.image(name='graph1.png', x=40, y =212, w = 180, h = 80, type = 'png')

pdf.print_chapter(2, 'Analysing the results', 'second_text.txt')
# final graphs for page 3
pdf.image(name='graph2.png', x=20, y =95, w = 170, h = 110, type = 'png')
pdf.image(name='graph3.png', x=20, y =200, w = 170, h = 90, type = 'png')


pdf.output('analysis.pdf')

# remove used image files from directory
extras = ['graph1.png', 'graph2.png', 'graph3.png']

for deadwood in extras:
    os.remove(deadwood)
