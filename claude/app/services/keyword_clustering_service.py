"""
Keyword Clustering Service (Back2 Day 2)
키워드 클러스터링 알고리즘 구현 (scipy 사용)
"""
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import json


class KeywordClusteringService:
    """
    키워드 클러스터링 서비스

    기능:
    - TF-IDF 기반 키워드 벡터화
    - K-Means 클러스터링
    - 계층적 클러스터링 (scipy)
    - 유사도 기반 키워드 그룹핑
    """

    def __init__(self):
        """Initialize clustering service"""
        self.vectorizer = None
        self.vectors = None

    def cluster_keywords(
        self,
        keywords: List[str],
        num_clusters: int = 5,
        method: str = "kmeans"
    ) -> Dict[str, any]:
        """
        키워드를 클러스터링합니다

        Args:
            keywords: 키워드 리스트
            num_clusters: 클러스터 개수
            method: 클러스터링 방법 ("kmeans" or "hierarchical")

        Returns:
            클러스터링 결과 딕셔너리
        """
        if not keywords or len(keywords) < 2:
            return {
                "clusters": [],
                "method": method,
                "num_keywords": len(keywords),
                "error": "최소 2개 이상의 키워드가 필요합니다"
            }

        # 키워드가 클러스터 수보다 적으면 클러스터 수 조정
        if len(keywords) < num_clusters:
            num_clusters = max(2, len(keywords) // 2)

        try:
            if method == "kmeans":
                result = self._kmeans_clustering(keywords, num_clusters)
            elif method == "hierarchical":
                result = self._hierarchical_clustering(keywords, num_clusters)
            else:
                raise ValueError(f"Unknown clustering method: {method}")

            return result

        except Exception as e:
            return {
                "clusters": [],
                "method": method,
                "num_keywords": len(keywords),
                "error": str(e)
            }

    def _kmeans_clustering(
        self,
        keywords: List[str],
        num_clusters: int
    ) -> Dict:
        """
        K-Means 클러스터링

        Args:
            keywords: 키워드 리스트
            num_clusters: 클러스터 개수

        Returns:
            클러스터링 결과
        """
        # TF-IDF 벡터화
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2),
            stop_words=None
        )

        # 키워드를 문자열로 결합 (TF-IDF는 문장 단위로 분석)
        keyword_texts = [kw.replace(" ", "_") for kw in keywords]
        self.vectors = self.vectorizer.fit_transform(keyword_texts)

        # K-Means 클러스터링
        kmeans = KMeans(
            n_clusters=num_clusters,
            random_state=42,
            n_init=10
        )
        cluster_labels = kmeans.fit_predict(self.vectors)

        # 클러스터별로 키워드 그룹화
        clusters = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(keywords[idx])

        # 클러스터 중심과의 거리 계산
        cluster_centers = kmeans.cluster_centers_
        cluster_info = []

        for cluster_id, cluster_keywords in clusters.items():
            # 클러스터 내 키워드들의 벡터 인덱스
            indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]

            # 클러스터 중심과의 평균 거리
            cluster_vectors = self.vectors[indices]
            center = cluster_centers[cluster_id]
            distances = cosine_similarity(cluster_vectors, center.reshape(1, -1))
            avg_coherence = float(np.mean(distances))

            # 대표 키워드 선택 (중심에 가장 가까운 키워드)
            representative_idx = indices[np.argmax(distances)]
            representative_keyword = keywords[representative_idx]

            cluster_info.append({
                "cluster_id": int(cluster_id),
                "representative_keyword": representative_keyword,
                "keywords": cluster_keywords,
                "coherence_score": round(avg_coherence, 3),
                "size": len(cluster_keywords)
            })

        # 클러스터를 크기 순으로 정렬
        cluster_info.sort(key=lambda x: x["size"], reverse=True)

        return {
            "method": "kmeans",
            "num_clusters": num_clusters,
            "num_keywords": len(keywords),
            "clusters": cluster_info,
            "success": True
        }

    def _hierarchical_clustering(
        self,
        keywords: List[str],
        num_clusters: int
    ) -> Dict:
        """
        계층적 클러스터링 (scipy 사용)

        Args:
            keywords: 키워드 리스트
            num_clusters: 클러스터 개수

        Returns:
            클러스터링 결과
        """
        # TF-IDF 벡터화
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2)
        )

        keyword_texts = [kw.replace(" ", "_") for kw in keywords]
        self.vectors = self.vectorizer.fit_transform(keyword_texts).toarray()

        # 거리 행렬 계산
        distances = pdist(self.vectors, metric='cosine')

        # 계층적 클러스터링 (Ward linkage)
        linkage_matrix = linkage(distances, method='ward')

        # 클러스터 할당 (덴드로그램 기반)
        from scipy.cluster.hierarchy import fcluster
        cluster_labels = fcluster(linkage_matrix, num_clusters, criterion='maxclust')

        # 클러스터별로 키워드 그룹화
        clusters = {}
        for idx, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(keywords[idx])

        # 클러스터 정보 구성
        cluster_info = []
        for cluster_id, cluster_keywords in clusters.items():
            # 클러스터 내 키워드 벡터들
            indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
            cluster_vectors = self.vectors[indices]

            # 클러스터 중심 계산
            center = np.mean(cluster_vectors, axis=0)

            # 중심과의 유사도 계산
            similarities = cosine_similarity(cluster_vectors, center.reshape(1, -1))
            avg_coherence = float(np.mean(similarities))

            # 대표 키워드
            representative_idx = indices[np.argmax(similarities)]
            representative_keyword = keywords[representative_idx]

            cluster_info.append({
                "cluster_id": int(cluster_id),
                "representative_keyword": representative_keyword,
                "keywords": cluster_keywords,
                "coherence_score": round(avg_coherence, 3),
                "size": len(cluster_keywords),
                "linkage_method": "ward"
            })

        # 클러스터를 크기 순으로 정렬
        cluster_info.sort(key=lambda x: x["size"], reverse=True)

        return {
            "method": "hierarchical",
            "num_clusters": num_clusters,
            "num_keywords": len(keywords),
            "clusters": cluster_info,
            "linkage_matrix": linkage_matrix.tolist(),  # 덴드로그램 데이터
            "success": True
        }

    def find_similar_keywords(
        self,
        target_keyword: str,
        keyword_pool: List[str],
        top_n: int = 5
    ) -> List[Tuple[str, float]]:
        """
        타겟 키워드와 유사한 키워드 찾기

        Args:
            target_keyword: 기준 키워드
            keyword_pool: 검색할 키워드 풀
            top_n: 반환할 상위 N개

        Returns:
            (키워드, 유사도) 튜플 리스트
        """
        if target_keyword not in keyword_pool:
            keyword_pool = [target_keyword] + keyword_pool

        # TF-IDF 벡터화
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(keyword_pool).toarray()

        # 타겟 키워드 벡터
        target_idx = keyword_pool.index(target_keyword)
        target_vector = vectors[target_idx].reshape(1, -1)

        # 코사인 유사도 계산
        similarities = cosine_similarity(vectors, target_vector).flatten()

        # 유사도가 높은 순으로 정렬 (자기 자신 제외)
        similar_indices = np.argsort(similarities)[::-1]
        similar_indices = [idx for idx in similar_indices if idx != target_idx]

        # 상위 N개 반환
        results = []
        for idx in similar_indices[:top_n]:
            results.append((keyword_pool[idx], float(similarities[idx])))

        return results

    def extract_key_phrases(
        self,
        text: str,
        top_n: int = 10
    ) -> List[Tuple[str, float]]:
        """
        텍스트에서 주요 구문 추출 (TF-IDF 기반)

        Args:
            text: 분석할 텍스트
            top_n: 반환할 상위 N개

        Returns:
            (구문, 점수) 튜플 리스트
        """
        # TF-IDF 벡터화 (1-gram, 2-gram)
        vectorizer = TfidfVectorizer(
            max_features=top_n * 2,
            ngram_range=(1, 2),
            stop_words=None
        )

        vectors = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()

        # TF-IDF 점수 추출
        scores = vectors.toarray()[0]

        # 점수가 높은 순으로 정렬
        top_indices = np.argsort(scores)[::-1][:top_n]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append((feature_names[idx], float(scores[idx])))

        return results


# Singleton instance
keyword_clustering_service = KeywordClusteringService()
