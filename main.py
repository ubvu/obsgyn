from scripts.pubmed import get_pubmeddata, clean_pubmeddata
import config.config as project_config

get_pubmeddata(mindate=project_config.year_start, maxdate=project_config.year_end)
clean_pubmeddata()


