#!/usr/bin/env python3
"""
参考文献链接验证脚本
验证 PubMed、DOI/Crossref 链接的有效性

用法:
    python verify_links.py --test-pubmed 21351269
    python verify_links.py --test-doi "10.1002/ijc.25516"
    python verify_links.py --help
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
import ssl
from typing import Dict, Optional, Tuple

# 配置
TIMEOUT = 10  # 秒
USER_AGENT = "MedBA-Journal-Typesetter/1.0 (mailto:contact@medbam.org)"
MAX_REDIRECTS = 3

def create_request(url: str, method: str = "GET") -> urllib.request.Request:
    """创建带有正确User-Agent的请求"""
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/html, */*"
        },
        method=method
    )

def verify_url(url: str) -> Tuple[bool, str, int]:
    """
    验证URL是否有效
    返回: (is_valid, status_message, http_code)
    """
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = create_request(url, "GET")
        
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as response:
            code = response.getcode()
            if code == 200:
                return True, "valid", code
            elif code in (301, 302, 303, 307, 308):
                return True, "valid (redirect)", code
            else:
                return False, f"unexpected status", code
                
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return False, "forbidden", 403
        elif e.code == 404:
            return False, "not_found", 404
        elif e.code == 429:
            return False, "rate_limited", 429
        else:
            return False, f"http_error", e.code
            
    except urllib.error.URLError as e:
        return False, f"connection_error: {str(e.reason)}", 0
        
    except TimeoutError:
        return False, "timeout", 0
        
    except Exception as e:
        return False, f"error: {str(e)}", 0

def verify_pubmed(pmid: str) -> Dict:
    """验证PubMed链接"""
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    is_valid, status, code = verify_url(url)
    
    return {
        "type": "pubmed",
        "pmid": pmid,
        "url": url,
        "valid": is_valid,
        "status": status,
        "http_code": code
    }

def verify_doi(doi: str) -> Dict:
    """通过Crossref API验证DOI是否存在"""
    # 清理DOI（移除可能的前缀）
    if doi.startswith("https://doi.org/"):
        doi = doi[16:]
    elif doi.startswith("http://doi.org/"):
        doi = doi[15:]
    elif doi.startswith("doi:"):
        doi = doi[4:]
    
    # 使用Crossref API验证DOI是否存在
    api_url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    
    try:
        ctx = ssl.create_default_context()
        req = create_request(api_url)
        
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode())
                if data.get("status") == "ok":
                    return {
                        "type": "crossref",
                        "doi": doi,
                        "url": f"https://doi.org/{doi}",
                        "valid": True,
                        "status": "valid",
                        "http_code": 200,
                        "title": data.get("message", {}).get("title", [""])[0]
                    }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                "type": "crossref",
                "doi": doi,
                "url": f"https://doi.org/{doi}",
                "valid": False,
                "status": "not_found",
                "http_code": 404
            }
    except Exception as e:
        pass
    
    return {
        "type": "crossref",
        "doi": doi,
        "url": f"https://doi.org/{doi}",
        "valid": False,
        "status": "api_error",
        "http_code": 0
    }

def search_pubmed_by_title(title: str) -> Optional[str]:
    """通过标题搜索PubMed获取PMID"""
    encoded_title = urllib.parse.quote(f"{title}[Title]")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={encoded_title}&retmode=json"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            data = json.loads(response.read().decode())
            id_list = data.get("esearchresult", {}).get("idlist", [])
            if id_list:
                return id_list[0]
    except Exception:
        pass
    
    return None

def generate_google_scholar_url(title: str) -> str:
    """生成Google Scholar搜索URL"""
    encoded_title = urllib.parse.quote(title)
    return f"https://scholar.google.com/scholar?q={encoded_title}"

def main():
    parser = argparse.ArgumentParser(
        description="验证参考文献链接有效性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --test-pubmed 21351269
  %(prog)s --test-doi "10.1002/ijc.25516"
  %(prog)s --search-pubmed "Estimates of worldwide burden of cancer"
        """
    )
    
    parser.add_argument(
        "--test-pubmed",
        metavar="PMID",
        help="测试PubMed链接 (提供PMID)"
    )
    
    parser.add_argument(
        "--test-doi",
        metavar="DOI",
        help="测试DOI链接 (提供DOI)"
    )
    
    parser.add_argument(
        "--search-pubmed",
        metavar="TITLE",
        help="通过标题搜索PubMed"
    )
    
    parser.add_argument(
        "--generate-scholar",
        metavar="TITLE",
        help="生成Google Scholar搜索URL"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出结果"
    )
    
    args = parser.parse_args()
    
    if not any([args.test_pubmed, args.test_doi, args.search_pubmed, args.generate_scholar]):
        parser.print_help()
        return 0
    
    results = []
    
    if args.test_pubmed:
        result = verify_pubmed(args.test_pubmed)
        results.append(result)
        if not args.json:
            status = "VALID" if result["valid"] else "INVALID"
            print(f"PubMed {args.test_pubmed}: {status} ({result['status']}, HTTP {result['http_code']})")
            print(f"URL: {result['url']}")
    
    if args.test_doi:
        result = verify_doi(args.test_doi)
        results.append(result)
        if not args.json:
            status = "VALID" if result["valid"] else "INVALID"
            print(f"DOI {args.test_doi}: {status} ({result['status']}, HTTP {result['http_code']})")
            print(f"URL: {result['url']}")
            if result.get("title"):
                print(f"Title: {result['title']}")
    
    if args.search_pubmed:
        pmid = search_pubmed_by_title(args.search_pubmed)
        result = {
            "type": "pubmed_search",
            "query": args.search_pubmed,
            "pmid": pmid,
            "found": pmid is not None
        }
        results.append(result)
        if not args.json:
            if pmid:
                print(f"Found PMID: {pmid}")
                print(f"URL: https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
            else:
                print("No PubMed match found")
    
    if args.generate_scholar:
        url = generate_google_scholar_url(args.generate_scholar)
        result = {
            "type": "google_scholar",
            "title": args.generate_scholar,
            "url": url,
            "status": "generated"
        }
        results.append(result)
        if not args.json:
            print(f"Google Scholar URL: {url}")
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    for r in results:
        if "valid" in r and not r["valid"]:
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
