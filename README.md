# spirograph
This is a Python3 implementation of a playground for creating images like the old-school Spirograph toy. It uses the pygame library, and also uses the Courier font if it can find it in the system.

Spirograph draws polar Fourier curves in up to four levels. You can control the number of levels, as well as the speed, radius, and angular displacement of each level. 

The implementation orbits a point around the center at a given speed, distance, and angular displacement. The next level orbits around that point at its own speed, distance, and angular displacement. The third level orbits that point, and the fourth level orbits that point. The combination of all of these orbits traces out a curve which is plotted. The first two levels of these curves give designs equivalent to those possible with a basic Spirograph set, which are various types of cycloid, epicycloid and hypocycloid curves. Adding additional levels adds some additional complexities not possible with the original toy. 

The goal of this playground is (1) to familiarize the user with these types of curves and with the effects of a Fourier series; (2) to make enjoyable generative art. To the latter end, you can control the colors with which the curves are plotted and also create patterns combining stepwise alteration of all of the parameters. 

Interface: Along the top are text fields in which the speed, radius, and angular displacement of each of the levels can be specified. These values can be negative and do not have to be integers. Levels 1 through 4 are color-coded blue, green, red, and yellow respectively; these colors have no relation to the color in which the curves are drawn, and are just used for easy visual identification of parameters. 

Below each of these fields are decrement/increment buttons (-/+). These can be used to automatically change the field values by the corresponding values set in the fields on the right. When you start the program, these fields are pre-populated with the value "0.1" as a speed increment; "10" for a radius increment; and "5" as angular increment. So, for example, if you press the "+" button below the blue (first level) radius field, with the second of the three blue fields at the right holding the default value “10”, the orbiting dot tracing out the circle will move 10 pixels farther from the center. If you press the “-” button, it will move 10 pixels inward. 

Levels are controlled by buttons within the level fields. When the program is launched, only level 1 is active. The level buttons for the other fields appear as narrow black rectangles within the value fields. To turn on a level, click the level button, and it will brighten. To turn it off, click the level button again.

The color selection tool allows you to select the current drawing color. The right portion of the color tool has a field which allows you to choose an increment by which the color will change. The default value is 2 pixels of hue. (Increment is only possible by hue; negative values are allowed. The cycle wraps around 360° of hue.) The value will remain constant when the color is incremented. To increment the color, press the “COLOR>” button. 

Most of the time, to create interesting artwork you will want to increment several things at once, multiple times. The “AUTO INC” button allows you to apply all of the currently set increments simultaneously, at whatever point you wish. You can wait until a curve cycles through its complete rotation, then press AUTO INC to redraw the curve with adjusted values, and repeat as often as you like. You may also choose to modify the curve before a cycle is complete. 

The preset increments are useful for exploring. When creating an artwork, you will usually want to reset the increments. The “RESET” button will clear all increments to zero, and also reset the settings for curves to their default values. 

To clear the curves drawn and start a new drawing, click the “CLEAR” button. 

The “||/>” button allows you to pause the generation of a curve. This is useful when you want to manually adjust several parameters simultaneously, without the curve drawing while parameters are only partly modified.

The “-/+” buttons below “RESOL.” allow you to control the resolution with which the curves are drawn. When exploring curve space, it may be useful to preview a curve at a low resolution (faster-drawing), then redraw it at a slower, higher resolution. The resolution is dependent on the speed settings for the levels. Clicking the “-” button will reduce the resolution by doubling the speed settings for all levels. The “+” button halves the speed for all levels. 

Pressing the spacebar when no field is selected (press RETURN to exit all fields) will toggle the curve-drawing to a fade-out mode. This is useful for observing the motion of the generating point, but will not produce any static artwork.

No input/output is implemented for saving artwork; screen-capture is recommended.



