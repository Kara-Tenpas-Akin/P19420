import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = random.sample(range(0, 100),1)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%m/%d %H:%M:%S'))
    #
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-10:]
    ys = ys[-10:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=5000)
plt.show()


