EX    = python3
FILE  = mmn_queue.py

all:
	for number in 0.50 0.90 0.95 0.99 ; do \
		$(EX) $(FILE) --lambd $$number --d $(d) ; \
	done

clean:
	for number in 0.5 0.9 0.95 0.99 ; do \
		rm out.txt_$$number ; \
	done