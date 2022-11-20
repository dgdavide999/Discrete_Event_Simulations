EX    = python3
SIM  = mmn_queue.py
GRA = graphics.py

all:
	for number in 0.50 0.90 0.95 0.99 ; do \
		$(EX) $(SIM) --lambd $$number --d $(d) ; \
	done
	$(EX) $(GRA)

graphics:
	$(EX) $(GRA)

clean:
	for number in 0.5 0.9 0.95 0.99 ; do \
		rm out.txt_$$number ; \
	done

#usage: 
# for executing and generating graphics: make all d='value'
# for generating only graphics: make graphics
# for deleting output files: make clean