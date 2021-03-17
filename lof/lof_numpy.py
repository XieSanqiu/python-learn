#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
lof
~~~~~~~~~~~~

This module implements the Local Outlier Factor algorithm.

:copyright: (c) 2013 by Damjan Kužnar.
:license: GNU GPL v2, see LICENSE for more details.

"""
import warnings

import numpy as np
from matplotlib import pyplot as plt


class LOF:
    """Helper class for performing LOF computations and instances
    normalization."""

    def __init__(self, instances, normalize=True):
        self.instances = instances
        self.normalize = normalize
        if normalize:
            self.normalize_instances()

    def compute_instance_attribute_bounds(self):
        max_values = np.max(self.instances, axis=0)
        min_values = np.min(self.instances, axis=0)

        diff = max_values - min_values
        if not np.all(diff):
            problematic_dimensions = ", ".join(str(i + 1) for i, v
                                               in enumerate(diff) if v == 0)
            warnings.warn("No data variation in dimensions: %s. You should "
                          "check your data or disable normalization."
                          % problematic_dimensions)

        self.max_attribute_values = max_values
        self.min_attribute_values = min_values

    def normalize_instances(self):
        """Normalizes the instances and stores the information for rescaling new instances."""
        if not hasattr(self, "max_attribute_values"):
            self.compute_instance_attribute_bounds()
        self.instances = (self.instances - self.min_attribute_values) / (self.max_attribute_values - self.min_attribute_values)
        self.instances[np.logical_not(np.isfinite(self.instances))] = 0


    def normalize_instance(self, instance):
        instance = (instance - self.min_attribute_values) / (self.max_attribute_values - self.min_attribute_values)
        instance[np.logical_not(np.isfinite(instance))] = 0
        return instance

    def local_outlier_factor(self, min_pts, instance):
        """The (local) outlier factor of instance captures the degree to which
        we call instance an outlier. min_pts is a parameter that is specifying a
        minimum number of instances to consider for computing LOF value.
        Returns: local outlier factor
        Signature: (int, float[:,:]) -> float"""
        if self.normalize:
            instance = self.normalize_instance(instance)
        return local_outlier_factor(min_pts, instance, self.instances)


def k_distance(k, instance, instances):
    """Computes the k-distance of instance as defined in paper. It also gatheres
    the set of k-distance neighbors.
    Returns: (k-distance, k-distance neighbors)
    Signature: (int, float[:,:]) -> (float, float[:,:])"""

    # compute Euclidean distances
    distances = np.sqrt(np.sum(np.power(instances - instance, 2), axis=1))

    sort_permutation = np.argsort(distances)
    distances = distances[sort_permutation]
    instances = instances[sort_permutation]

    # real_k = np.unique(distances)  #不能有重复值
    real_k = distances  # 可以有重复值
    real_k = real_k[k - 1] if len(real_k) >= k else real_k[-1]
    neighbors = instances[distances <= real_k, :]

    k_distance_value = distances[
        k - 1] if len(distances) >= k else distances[-1]
    return k_distance_value, neighbors


def reachability_distance(k, instance1, instance2, instances):
    """The reachability distance of instance1 with respect to instance2.
    Returns: reachability distance
    Signature: (int, float[:], float[:], float[:,:]) -> float"""
    (k_distance_value, neighbors) = k_distance(k, instance2, instances)
    return max([k_distance_value, np.sqrt(np.sum(np.power(instance1 - instance2, 2)))])


def local_reachability_density(min_pts, instance, instances):  # , **kwargs):
    """Local reachability density of instance is the inverse of the average
    reachability distance based on the min_pts-nearest neighbors of instance.
    Returns: local reachability density
    Signature: (int, float[:], float[:,:]) -> float"""
    (k_distance_value, neighbors) = k_distance(min_pts, instance, instances)
    reachability_distances_array = [0] * len(neighbors)
    for i, neighbour in enumerate(neighbors):
        reachability_distances_array[i] = reachability_distance(min_pts, instance, neighbour, instances)
    if not any(reachability_distances_array):
        warnings.warn("Instance %s (could be normalized) is identical to all "
                      "the neighbors. Setting local reachability density to "
                      "inf." % repr(instance))
        return float("inf")
    else:
        return len(neighbors) / sum(reachability_distances_array)


def local_outlier_factor(min_pts, instance, instances):
    """The (local) outlier factor of instance captures the degree to which we
    call instance an outlier. min_pts is a parameter that is specifying a
    minimum number of instances to consider for computing LOF value.
    Returns: local outlier factor
    Signature: (int, float[:], float[:,:]) -> float"""
    (k_distance_value, neighbors) = k_distance(min_pts, instance, instances)
    instance_lrd = local_reachability_density(min_pts, instance, instances)
    lrd_ratios_array = [0] * len(neighbors)
    for i, neighbour in enumerate(neighbors):
        # instances_without_instance = instances[(instances != neighbour).any(axis=1)] #去除所有与neighbour相等的值
        aim_idx = np.where(instances == neighbour)[0][0]
        instances_without_instance = np.delete(instances, aim_idx, axis=0) #去除与neighbour相等的一个值

        neighbour_lrd = local_reachability_density(min_pts, neighbour, instances_without_instance)
        lrd_ratios_array[i] = neighbour_lrd / instance_lrd
    return sum(lrd_ratios_array) / len(neighbors)


def outliers(k, instances, normalize=True):
    """Simple procedure to identify outliers in the dataset."""
    instances_value_backup = np.copy(instances)
    outliers = []
    for i, instance in enumerate(instances_value_backup):
        instances = np.copy(instances_value_backup)
        instances = np.delete(instances, i, axis=0)
        l = LOF(instances, normalize=normalize)
        value = l.local_outlier_factor(k, instance)
        if value > 1:
            outliers.append({"lof": value, "instance": instance, "index": i})
    outliers.sort(key=lambda o: o["lof"], reverse=True)
    return outliers

instances = [
 (-4.8447532242074978, -5.6869538132901658),
 (1.7265577109364076, -2.5446963280374302),
 (-1.9885982441038819, 1.705719643962865),
 (-1.999050026772494, -4.0367551415711844),
 (-2.0550860126898964, -3.6247409893236426),
 (-1.4456945632547327, -3.7669258809535102),
 (-4.6676062022635554, 1.4925324371089148),
 (-3.6526420667796877, -3.5582661345085662),
 (6.4551493172954029, -0.45434966683144573),
 (-0.56730591589443669, -5.5859532963153349),
 (-5.1400897823762239, -1.3359248994019064),
 (5.2586932439960243, 0.032431285797532586),
 (6.3610915734502838, -0.99059648246991894),
 (-0.31086913190231447, -2.8352818694180644),
 (1.2288582719783967, -1.1362795178325829),
 (-0.17986204466346614, -0.32813130288006365),
 (2.2532002509929216, -0.5142311840491649),
 (-0.75397166138399296, 2.2465141276038754),
 (1.9382517648161239, -1.7276112460593251),
 (1.6809250808549676, -2.3433636210337503),
 (0.68466572523884783, 1.4374914487477481),
 (2.0032364431791514, -2.9191062023123635),
 (-1.7565895138024741, 0.96995712544043267),
 (3.3809644295064505, 6.7497121359292684),
 (-4.2764152718650896, 5.6551328734397766),
 (-3.6347215445083019, -0.85149861984875741),
 (-5.6249411288060385, -3.9251965527768755),
 (4.6033708001912093, 1.3375110154658127),
 (-0.685421751407983, -0.73115552984211407),
 (-2.3744241805625044, 1.3443896265777866)]

def test1():
    plt.style.use('ggplot')
    x, y = zip(*instances)
    plt.scatter(x, y, 20, color="#0000FF")
    my_lof = LOF(instances)

    for instance in [[0, 0], [5, 5], [10, 10], [-8, -8]]:
        value = my_lof.local_outlier_factor(5, instance)
        color = "#FF0000" if value > 1 else "#00FF00"
        plt.scatter(instance[0], instance[1], color=color, s=(value - 1) ** 2 * 10 + 20)
        print(value, instance)
    plt.show()

def test2():
    plt.style.use('ggplot')

    x, y = zip(*instances)
    plt.scatter(x, y, 20, color="#0000FF")

    my_lof = outliers(5, instances)
    print(len(my_lof), my_lof)

    for outlier in my_lof:
        value = outlier["lof"]
        instance = outlier["instance"]
        color = "#FF0000" if value > 2 else "#00FF00"
        plt.scatter(instance[0], instance[1], color=color, s=(value - 2) ** 2 * 10 + 20)

    plt.show()

if __name__ == '__main__':
    # test1()
    test2()