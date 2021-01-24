import sys


def ingest_image_file(filename):
    img_set = set()
    with open(filename, "r") as img_file:
        for line in img_file:
            pathparts = line.split("/")
            filename = pathparts[-1]
            img_set.add(filename)
    return img_set


def output_file_delta_list(input_filename, output_filename, delta_set):
    output_set = set()
    with open(input_filename, "r") as input_file:
        for line in input_file:
            pathparts = line.split("/")
            nodir_filename = pathparts[-1]
            if nodir_filename in delta_set:
                output_set.add(line)
    with open(output_filename, "w") as out_file:
        out_file.writelines(sorted(output_set))


def compare_image_set(img_set, img_fn, comp_set, comp_fn):
    only_in_img_set = img_set.difference(comp_set)
    only_in_comp_set = comp_set.difference(img_set)
    in_both = img_set.intersection(comp_set)
    print("{} images present only in {}".format(len(only_in_img_set), img_fn))
    print("{} images present only in {}".format(len(only_in_comp_set), comp_fn))
    print("{} images present in both files".format(len(in_both)))
    output_file_delta_list(img_fn, "file_1_only.txt", only_in_img_set)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        image_filename = sys.argv[1]
        image_set = ingest_image_file(image_filename)
        compare_to_filename = sys.argv[2]
        comparison_set = ingest_image_file(compare_to_filename)
        compare_image_set(image_set, image_filename, comparison_set, compare_to_filename)
    else:
        print("Usage: image_list_file comparison_file")
