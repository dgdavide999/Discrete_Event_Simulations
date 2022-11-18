EX		= python3
FILE	= mmn_queue.py

1:
	for number in 0.50 0.90 0.95 0.99 ; do \
		$(EX) $(FILE) --lambd $$number --d 1 ; \
	done

2:
	for number in 0.50 0.90 0.95 0.99 ; do \
		$(EX) $(FILE) --lambd $$number --d 2 ; \
	done

5:
	for number in 0.50 0.90 0.95 0.99 ; do \
		$(EX) $(FILE) --lambd $$number --d 5 ; \
	done

10:
	for number in 0.50 0.90 0.95 0.99 ; do \
		$(EX) $(FILE) --lambd $$number --d 10 ; \
	done

clean:
	rm **/$(OUT)