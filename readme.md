On linux: `docker run -v $(pwd):/runtime/app aciobanu/scrapy`

On windows: 

    To Run `docker run -v %cd%:/runtime/app aciobanu/scrapy`
    To Crawl `docker run -v %cd%:/runtime/app aciobanu/scrapy crawl dcaRegistry -o data/dca.json`
    
    