import csv


def csv_to_eav(read_file='Schedule.csv', write_file='Schedule_EAV.csv'):
    with open(read_file, 'r', newline='', encoding='utf-8') as ifp, open(write_file, 'w', newline='') as ofp:
        reader = csv.reader(ifp)
        writer = csv.writer(ofp)

        header = next(reader)

        for i, row in enumerate(reader, start=1):
            for col, val in zip(header, row):
                if col == 'Ώρα':
                    new_vals = val.split('-')
                    writer.writerow([i, 'Ώρα Έναρξης', new_vals[0]])
                    writer.writerow([i, 'Ώρα Λήξης', new_vals[1]])
                else:
                    writer.writerow([i, col, val])


def eav_to_graph(read_file='Schedule_EAV.csv', write_file='Schedule_Graph.csv'):
    with open(read_file, newline='') as ifp, open(write_file, 'w', newline='') as ofp:
        reader = csv.reader(ifp)
        writer = csv.writer(ofp)

        for s, p, o in reader:
            new_s, new_o = 'b:' + s, o
            if p in ['Μάθημα', 'Αίθουσα', 'Διδάσκων']:
                new_o = 'u:' + o
            else:
                new_o = 'l:' + o
            writer.writerow([new_s, p, new_o])


def graph_to_uri(read_file='Schedule_Graph.csv', write_file='Schedule_URI.csv', host='host', name='p15zerv'):
    def encode_char(char):
        if char in to_encode:
            return '%' + hex(ord(char))[2:]
        return char

    def encode_string(string):
        new_s = ''
        for char in string:
            new_s += encode_char(char)
        return new_s

    base_uri = f"http://{host}/sw/{name}"
    to_encode = {
        ':', '/', '?', '#', '[', ']', '@', '!', '$', '&', "'",
        '(', ')', '*', '+', ',', ';', '=', '<', '>', '"', ' ',
        '{', '}', '|', '\\', '^', '`'
    }

    with open(read_file, newline='') as ifp, open(write_file, 'w', newline='') as ofp:
        reader = csv.reader(ifp)
        writer = csv.writer(ofp)

        for s, p, o in reader:
            new_p = base_uri + '/myvocab#' + encode_string(p)
            if 'u:' == o[:2]:
                new_o = f'{base_uri}/resource/{encode_string(o[2:])}'
            else:
                new_o = o
            writer.writerow([s, new_p, new_o])


def uri_to_rdf(read_file='Schedule_URI.csv', write_file='Schedule_RDF.nt'):
    with open(read_file, newline='') as ifp, open(write_file, 'w') as ofp:
        reader = csv.reader(ifp)

        for s, p, o in reader:
            new_s = f'_:b{s[2:]}'
            new_p = f'<{p}>'
            if o[:2] == 'l:':
                new_o = o[2:]
                if 'Ώρα' in p:
                    new_o += ':00'
                new_o = f'"{new_o}"'
            else:
                new_o = f'<{o}>'
            ofp.write(' '.join([new_s, new_p, new_o]) + ' .\n')


if __name__ == '__main__':
    csv_to_eav()
    eav_to_graph()
    graph_to_uri()
    uri_to_rdf()
