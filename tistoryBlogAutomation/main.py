from crawlingManager import runCrawlingManager
from gptManager import requestGptAPI
from tblogManager import runTblogManager, writeContentByGptResult, bodystyling_update, publish_newpost

#1 tistory 블로그에 로그인 구현
runTblogManager()
#2 techcrunch 사이트에 해당 포스트의 정보들을 긁어오는 크롤링을 구현
contents_crawling_result = runCrawlingManager()
#3 크롤링한 결과를 gptapi에 입력 후 요청
gpt_result = requestGptAPI(contents_crawling_result)

#4 gpt 결과를 read해서 블로그의 제목과 본문을 입력
writeContentByGptResult(gpt_result)
#5 본문 스타일링 조작 구현
bodystyling_update()

#6 완성글 발행 조작 구현
publish_newpost()