import streamlit as st
from code.search_engine import process_query


st.write(
"""
# Check news from different sources 
"""
)


input_side, button_side = st.columns([0.8, 0.2])
with input_side:
    st.text_input("Input a new's url", placeholder="https://webnews.com/....", key="query")

with button_side:
    st.write('<style> .button-container { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 90%; } </style>', unsafe_allow_html=True)
    st.write('<div class="button-container">', unsafe_allow_html=True)
    st.button('Search', key="search_button")
    st.write('</div>', unsafe_allow_html=True)


if st.session_state.search_button and st.session_state.query:
    print("Procesando la consulta...")
    article, news = process_query(st.session_state.query)
    
    named_entities = {}
    
    for text, entity in article.named_entities:
        if entity in named_entities.keys():
            named_entities[entity].append(text)
        else:
            named_entities[entity] = [text]

    if len(news) > 0:        
        st.caption("#### The provided new")
        st.markdown(f"""
            ##### [{article.title}]({article.url})
            **{', '.join(article.authors)}** | {article.publish_date}
        """)
        st.markdown(f"""
            **Named Entities:** 
        """)
        st.write(article.summary)
        for entity in named_entities.keys():
            values = list(set(named_entities[entity])) 
            st.caption(f"_{entity}_: {', '.join(values)}")
        st.write("\n\n\n")
            
        st.divider()
        st.caption("#### Suggestions")
        for new, relevance in news:
            st.caption(f"RELEVANCE: {round(relevance, 4)}")
            st.markdown(f"""
                ##### [{new.title}]({new.url})
                **{new.authors}** | {new.publish_date}
                
                {new.description}
            """)
            st.write("\n\n\n")
            st.divider()
    else:
        st.image('not-found.jpeg', use_column_width=True)
