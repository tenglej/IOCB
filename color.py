from pymol import cmd


def style_selection(sel="sele"):

    # show sticks for selection
    cmd.show("sticks", sel)

    # element-based coloring
    cmd.color("grey90", sel + " and elem C")
    cmd.color("grey90", sel + " and elem H")
    cmd.color("red",    sel + " and elem O")
    cmd.color("blue",   sel + " and elem N")
    cmd.color("orange", sel + " and elem S")

    # everything else as cartoon
    cmd.hide("everything", "not " + sel)
    cmd.show("cartoon", "all")

    # transparency for cartoon
    cmd.set("cartoon_transparency", 0.5)

    # background
    cmd.bg_color("white")


# run
style_selection()
