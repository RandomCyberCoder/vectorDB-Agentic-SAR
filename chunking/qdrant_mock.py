#this is a mock file to test qdrant locally
#it assumes you have qdrant running locally on default port 6333
#for example using docker:
# docker pull qdrant/qdrant
# docker run -d -p 6333:6333 -p 6334:6334 \
#     -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
#     --name qdrant-mock qdrant/qdrant

from xmlrpc import client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue


client = QdrantClient(url="http://localhost:6333")

def create_collection():
    
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )
    operation_info = client.upsert(
        collection_name="test_collection",
        wait=True,
        points=[
            PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin",
                                                                        "provenance": {"source": "Unknown",
                                                                                       "author": "Unknown"},
                                                                        "content": "This is a sample text about Berlin."}),
            PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London",
                                                                        "provenance": {"source": "Unknown",
                                                                                       "author": "Unknown"},
                                                                        "content": "This is a sample text about London."}),
            PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow",
                                                                        "provenance": {"source": "Unknown",
                                                                                       "author": "Unknown"},
                                                                        "content": "This is a sample text about Moscow."}),
            PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York",
                                                                        "provenance": {"source": "Unknown",
                                                                                       "author": "Unknown"},
                                                                        "content": "This is a sample text about New York."}),
            PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing",
                                                                        "provenance": {"source": "Unknown",
                                                                                       "author": "Unknown"},
                                                                        "content": "This is a sample text about Beijing."}),
            PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai",
                                                                        "provenance": {"source": "Unknown",
                                                                                       "author": "Unknown"},
                                                                        "content": "This is a sample text about Mumbai."}
                                                                    ),
        ],
    )

    print(operation_info)




if __name__ == '__main__':
    create_collection()
    search_result = client.query_points(
        collection_name="test_collection",
        query=[0.2, 0.1, 0.9, 0.7],
        with_payload=True,
        limit=3
    ).points

    print(search_result)

    search_result = client.query_points(
        collection_name="test_collection",
        query=[0.2, 0.1, 0.9, 0.7],
        query_filter=Filter(
            must=[FieldCondition(key="city", match=MatchValue(value="London"))]
        ),
        with_payload=True,
        limit=3,
    ).points

    print(search_result)
    client.delete_collection(collection_name="test_collection") 
    print(f"Collection 'my_collection_name' deleted.")