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
from sentence_transformers import SentenceTransformer


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
    #assuming SAR_collection already exists
    model = SentenceTransformer("all-MiniLM-L6-v2")
    summary = (
    "The matched incidents involve searches for youth subjects engaged in outdoor activities such as hiking and hunting across different terrains—primarily mountainous and flat areas, with two incidents physically taking place in flat terrains. All three incidents resulted in successful outcomes, with subjects being found alive.\n\n"
    "Key patterns relevant to the query include:\n"
    "- Outcome: All cases involved active search efforts, aligning with the 'search' outcome specified.\n"
    "- Terrain: Two incidents occurred on flat terrain, matching the 'flat' terrain criteria, while one involved mountainous terrain.\n"
    "- Subject Category and Activity: All subjects were youths, consistent with the category specified, engaged in outdoor activities like hiking and hunting, which are common adventures for youth in search and rescue scenarios.\n"
    "- Age and Well-being: The ages ranged from 8 to 15, with all subjects reported to be well, indicating effective rescue operations.\n\n"
    "Overall, these incidents exemplify successful search efforts for young individuals involved in outdoor activities within flat terrains, directly corresponding to the search and rescue query focusing on youth in flat terrains.\n"
    "Where to locate a missing person based on the summary above"
    )
    embedding = model.encode(summary).tolist()
    search_result = client.query_points(
        collection_name="SAR_collection",
        query=embedding,
        with_payload=True,
        limit=3
    ).points

    for point in [point.payload for point in search_result]:
        print(point, "\n\n")

    # print([x for point in search_result for x in point.payload.dict()])
    # create_collection()
    # search_result = client.query_points(
    #     collection_name="test_collection",
    #     query=[0.2, 0.1, 0.9, 0.7],
    #     with_payload=True,
    #     limit=3
    # ).points

    # print(search_result)

    # search_result = client.query_points(
    #     collection_name="test_collection",
    #     query=[0.2, 0.1, 0.9, 0.7],
    #     query_filter=Filter(
    #         must=[FieldCondition(key="city", match=MatchValue(value="London"))]
    #     ),
    #     with_payload=True,
    #     limit=3,
    # ).points

    # print(search_result)
    # client.delete_collection(collection_name="test_collection") 
    # print(f"Collection 'my_collection_name' deleted.")