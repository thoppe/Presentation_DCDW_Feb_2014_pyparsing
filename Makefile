target = "DCDW_pyparsing.markdown"

# May need to run twice on first pull to copy styles
all:
	python easy_pres.py $(target) --output index.html

edit:
	emacs $(target) &

push:
	git status
	git add index.html
	git add css
	git add js
	git add *.markdown
	git commit -a
	git push

pull:
	git pull
view:
	chromium-browser index.html
clean:
	rm -rvf css js index.html