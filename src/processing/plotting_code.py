import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def top_adj(new_adj, formal_adj):
    # Plot new_adj
    fig = plt.figure(figsize=(11, 7))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.5)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_facecolor('#ededed')
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray",
                  linestyle="dashed",
                  alpha=0.2)
    fig.patch.set_facecolor("#ededed")
    plt.xticks(fontsize=16)
    plt.yticks([i*.5 for i in range(7)], fontsize=16)
    ax.set_ylim([0,3.1])
    plt.xlabel("Word", fontsize=18)
    plt.ylabel("Percent", fontsize=18)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.title('Modern Adjectives (Top 10)', fontsize=22,loc="right")
    plt.bar(x=new_adj.head(10)["Word"],
            height=new_adj.head(10)["Count"],
            color="#c43d3d",
            width=.75)
    plt.savefig("figures/modern_adj.png")
    plt.clf()


    #Plot formal_adj
    fig = plt.figure(figsize=(11, 7))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.5)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_facecolor('#ededed')
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray",
                  linestyle="dashed",
                  alpha=0.2)
    fig.patch.set_facecolor("#ededed")
    plt.xticks(fontsize=16)
    plt.yticks([i*.5 for i in range(7)], fontsize=16)
    ax.set_ylim([0,3.1])
    plt.xlabel("Word", fontsize=18)
    plt.ylabel("Percent", fontsize=18)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.title('Modern Adjectives (Top 10)', fontsize=22,loc="right")
    plt.bar(x=formal_adj.head(10)["Word"],
            height=formal_adj.head(10)["Count"],
            color="#3d6fbf",
            width=.75)
    plt.savefig("figures/formal_adj.png")


def prop_adjectives(formal_prop, modern_prop):
    plt.clf()
    fig = plt.figure(figsize=(8, 7))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.5)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_facecolor('#ededed')
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray",
                  linestyle="dashed",
                  alpha=0.2)
    fig.patch.set_facecolor("#ededed")
    plt.xticks(fontsize=16)
    plt.yticks([i*3 for i in range(6)], fontsize=16)
    ax.set_ylim([0,16])
    plt.xlabel("Writing style", fontsize=18)
    plt.ylabel("Percent", fontsize=18)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.title('Proportion of Adjectives to Total Words', fontsize=22,loc="center")
    bars = plt.bar(x=["Formal", "Modern"],
                   height=[formal_prop, modern_prop],
                   color=["#3d6fbf", "#c43d3d"],
                   width=.8)
    plt.savefig("figures/formal_modern.png")

def pos_props(new_text, formal_text):
    import squarify
    modern_pos_prop = new_text.groupby("POS", as_index=False).sum()
    formal_pos_prop = formal_text.groupby("POS", as_index=False).sum()

    modern_pos_prop = modern_pos_prop.drop([0,11])
    modern_total = modern_pos_prop["Count"].sum()


    modern_pos_prop = modern_pos_prop.sort_values(["Count"], ascending=False)
    modern_pos_prop["Count"] = round(modern_pos_prop["Count"]/modern_total*100, 2)

    color_list = ["#7aa9f5", "#7dd6e8", "#00ffc3", "#59cf86", "#a1d177", "#eaf0a8", "#ffd0a1", "#ff8f57", "#ff5454", "#ff6be4"]
    modern_pos_prop["POS"] = modern_pos_prop["POS"].str.capitalize()

    tiny_tags = [4,5,8,9]
    labels = modern_pos_prop["POS"]+"\n"+modern_pos_prop["Count"].astype(str) + "%"
    legend_labels = modern_pos_prop.drop([i for i in range(1,11) if i not in tiny_tags])
    legend_labels = legend_labels["POS"]+"\n"+legend_labels["Count"].astype(str) + "%"
    legend_labels = legend_labels.to_list()
    labels = labels.drop(tiny_tags)

    ax = squarify.plot(sizes=modern_pos_prop["Count"],
                       label=labels,
                       color=color_list,
                       alpha=0.8,
                       edgecolor="white",
                       linewidth=3,
                       text_kwargs={'fontsize':11})
    plt.axis('off')
    plt.legend(handles=ax.containers[0][6:10],
               labels=legend_labels,
               handlelength=1,
               handleheight=1,
               fontsize=10,
               loc="lower left",
               bbox_to_anchor=(-0.05,-0.05))
    plt.title("Percent of Modern Words", fontsize=15)
    plt.savefig("figures/modern_pos_proportions.png")

    plt.clf()

    formal_pos_prop = formal_pos_prop.drop([0,11])
    formal_total = formal_pos_prop["Count"].sum()


    formal_pos_prop = formal_pos_prop.sort_values(["Count"], ascending=False)
    formal_pos_prop["Count"] = round(formal_pos_prop["Count"]/formal_total*100, 2)

    color_list = ["#7aa9f5", "#7dd6e8", "#00ffc3", "#59cf86", "#a1d177", "#eaf0a8", "#ffd0a1", "#ff8f57", "#ff5454", "#ff6be4"]
    formal_pos_prop["POS"] = formal_pos_prop["POS"].str.capitalize()

    tiny_tags = [4,5,8,9]
    labels = formal_pos_prop["POS"]+"\n"+formal_pos_prop["Count"].astype(str) + "%"
    legend_labels = formal_pos_prop.drop([i for i in range(1,11) if i not in tiny_tags])
    legend_labels = legend_labels["POS"]+"\n"+legend_labels["Count"].astype(str) + "%"
    legend_labels = legend_labels.to_list()
    labels = labels.drop(tiny_tags)

    ax = squarify.plot(sizes=formal_pos_prop["Count"],
                       label=labels,
                       color=color_list,
                       alpha=0.8,
                       edgecolor="white",
                       linewidth=3,
                       text_kwargs={'fontsize':11})
    plt.axis('off')
    plt.legend(handles=ax.containers[0][6:10],
               labels=legend_labels,
               handlelength=1,
               handleheight=1,
               fontsize=10,
               loc="lower left",
               bbox_to_anchor=(-0.05,-0.05))
    plt.title("Percent of Formal Words", fontsize=15)
    plt.savefig("figures/formal_pos_proportions.png")
