# Makefile for Astrophysics Course Companion

MAIN = AstroPhysics
FIG_SRC_DIR = fig_sources
FIG_OUT_DIR = figs
FIG_SRCS = $(wildcard $(FIG_SRC_DIR)/*.tex)
FIG_PDFS = $(patsubst $(FIG_SRC_DIR)/%.tex, $(FIG_OUT_DIR)/%.pdf, $(FIG_SRCS))

.PHONY: all pdf figs clean quick

all: pdf

pdf: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex $(FIG_PDFS)
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex

quick:
	pdflatex -interaction=nonstopmode $(MAIN).tex

figs: $(FIG_PDFS)

$(FIG_OUT_DIR)/%.pdf: $(FIG_SRC_DIR)/%.tex
	@mkdir -p $(FIG_OUT_DIR)
	pdflatex -interaction=nonstopmode -output-directory=$(FIG_OUT_DIR) $<

clean:
	rm -f *.aux *.log *.out *.toc *.synctex.gz *.fdb_latexmk *.fls $(FIG_OUT_DIR)/*.aux $(FIG_OUT_DIR)/*.log
