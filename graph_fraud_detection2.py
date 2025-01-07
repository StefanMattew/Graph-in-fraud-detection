import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Dataset awal

data = {
    'number_1': [
        '081234567890', '081234567890', '081234560456', '081234567789', '081234567789', 
        '081234560456', '081234561111', '081234562222', '081234563333', '081234564444', 
        '081234565555', '081234566666', '081234567777', '081234568888', '081234569999', 
        '081234561111', '081234562222', '081234570000', '081234571111', '081234572222', 
        '081234573333', '081234574444', '081234575555', '081234576666', '081234577777'
    ],
    'number_2': [
        '081234560456', '081234567789', '081234567789', '081234560321', '081234560654', 
        '081234560321', '081234563333', '081234564444', '081234565555', '081234566666', 
        '081234567777', '081234568888', '081234569999', '081234561111', '081234562222', 
        '081234570000', '081234571111', '081234572222', '081234573333', '081234574444', 
        '081234575555', '081234576666', '081234577777', '081234567890', '081234560456'
    ],
    'tags_1': [
        ['Penipu', 'Spam Call'], ['Penipu', 'Asuransi'], ['Joko'], ['Doni'], ['Spam Call'], 
        ['Asuransi'], ['Penipu'], ['Budi'], ['Asuransi'], ['Marketing'], 
        ['Penipu'], ['Doni'], ['Joko'], ['Penagih Utang'], ['Penipu'], 
        ['Spam Call'], ['Penipu', 'Marketing'], ['Asuransi'], ['Doni'], ['Joko'], 
        ['Budi', 'Spam Call'], ['Penagih Utang'], ['Marketing'], ['Sales'], ['Penipu']
    ],
    'tags_2': [
        ['Joko'], ['Spam Call'], ['Spam Call'], ['Penipu'], ['Penipu'], 
        ['Doni'], ['Spam Call'], ['Penipu'], ['Penipu'], ['Sales'], 
        ['Budi'], ['Doni'], ['Marketing'], ['Penipu'], ['Asuransi'], 
        ['Penipu', 'Joko'], ['Budi'], ['Spam Call'], ['Penagih Utang'], ['Sales'], 
        ['Penipu'], ['Asuransi'], ['Marketing'], ['Doni'], ['Joko']
    ]
}


# membuat dataframe dari dataset 
df = pd.DataFrame(data)

# Mencari tag yang berisi "Penipu"
penipu_data = df[df['tags_1'].apply(lambda tags: 'Penipu' in tags) | df['tags_2'].apply(lambda tags: 'Penipu' in tags)]

# membuat graf jaringan penipu
G = nx.Graph()

for idx, row in penipu_data.iterrows():
    G.add_edge(row['number_1'], row['number_2'], tags_1=row['tags_1'], tags_2=row['tags_2'])

# Menambah simpul graf
for node in G.nodes():
    tags = set()
    for idx, row in penipu_data.iterrows():
        if row['number_1'] == node:
            tags.update(row['tags_1'])
        if row['number_2'] == node:
            tags.update(row['tags_2'])
    G.nodes[node]['tags'] = ', '.join(tags)

# menentuakan warna simpul berdasarkan tag
node_colors = []
for node, attr in G.nodes(data=True):
    if 'Penipu' in attr['tags']:
        # WARna penipu diberi warna merah
        node_colors.append('red') 

    else:
        # warna bukan penipu tidak diberi merah     
        node_colors.append('skyblue') 

# Menampilkan graf
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=700,
    node_color=node_colors, 
    font_size=10,
    font_color='black',  
)

plt.show()

# Daftar Penipu
fraud_list = []
for node, attr in G.nodes(data=True):
    if 'Penipu' in attr['tags']:
        fraud_list.append(node)

print("Daftar Penipu:", fraud_list)


# Fungsi mencari tag berdasar nomor
def search_tags(number):
    tags = set()
    for idx, row in penipu_data.iterrows():
        if row['number_1'] == number:
            tags.update(row['tags_1'])
        if row['number_2'] == number:
            tags.update(row['tags_2'])
    return list(tags)



# mengetes nomor dengna fungsi search_tags
input_number = '0'
while input_number != 'q' :
    input_number = (input("Masukkan nomor telepon(ketik 'q' untuk quit): "))
    
    result_tags = search_tags(input_number)

    if result_tags:
        print(f"Tag untuk nomor {input_number}: {result_tags}")
    
    else:
        print(f"Tidak ditemukan tag untuk nomor {input_number}.")
