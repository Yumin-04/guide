#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from typing import Dict, List


def process_file_data(input_path: Path, keywords: List[str]) -> Dict[str, int]:
    """
    지정한 파일에서 키워드의 출현 빈도를 카운트하는 함수입니다.

    :param input_path: 분석할 파일의 pathlib.Path 객체
    :param keywords: 검색할 키워드 리스트
    :return: 키워드별 빈도수를 담은 딕셔너리 (반환 타입 필수 명시)
    """
    results: Dict[str, int] = {keyword: 0 for keyword in keywords}

    # 파일 존재 여부 확인 (pathlib 네이티브 메서드 활용)
    if not input_path.exists():
        print(f"Warning: 파일이 존재하지 않습니다: {input_path}")
        return results

    try:
        content = input_path.read_text(encoding="utf-8")
        for keyword in keywords:
            results[keyword] = content.count(keyword)
    except (IOError, OSError) as e:
        # Exception 대신 구체적인 예외 타입 지정
        print(f"Error reading file: {e}")

    return results


def setup_cli() -> argparse.Namespace:
    """
    명령행 인자(CLI)를 파싱하고 도움말(CLI Help)을 생성하는 함수입니다.

    :return: 파싱된 인자 객체 (argparse.Namespace)
    """
    parser = argparse.ArgumentParser(
        description="pathlib, argparse, typing을 활용한 데이터 분석 툴"
    )

    parser.add_argument(
        "-i", "--input",
        type=Path,
        metavar="FILE",           # --help 출력 시 인자 역할 명확화
        required=True,
        help="분석할 입력 파일의 경로를 지정합니다. (필수)"
    )

    parser.add_argument(
        "-k", "--keywords",
        type=str,
        nargs="+",
        metavar="KEYWORD",        # --help 출력 시 인자 역할 명확화
        required=True,
        help="검색할 하나 이상의 키워드를 공백으로 구분하여 입력합니다. (필수)"
    )

    return parser.parse_args()


def main() -> None:
    """
    프로그램의 메인 진입점 함수입니다. 반환값이 없으므로 None을 명시합니다.
    """
    args = setup_cli()

    analysis_results = process_file_data(
        input_path=args.input,
        keywords=args.keywords
    )

    print("\n=== 분석 결과 ===")
    for word, count in analysis_results.items():
        print(f" - {word}: {count}회 발견")


if __name__ == "__main__":
    main()
