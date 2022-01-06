import tensorflow as tf
from keras_cv.layers.preprocessing.cut_mix import CutMix


NUM_CLASSES = 10


class CutMixTest(tf.test.TestCase):
    def test_return_shapes(self):
        xs = tf.ones((2, 512, 512, 3))
        # randomly sample labels
        ys = tf.random.categorical(tf.math.log([[0.5, 0.5]]), 2)
        ys = tf.squeeze(ys)
        ys = tf.one_hot(ys, NUM_CLASSES)

        layer = CutMix(probability=1.0)
        xs, ys = layer(xs, ys)

        self.assertEqual(xs.shape, [2, 512, 512, 3])
        # one hot smoothed labels
        self.assertEqual(ys.shape, [2, 10])
        self.assertEqual(len(ys != 0.0), 2)

    def test_label_smoothing(self):
        xs = tf.ones((2, 512, 512, 3))
        # randomly sample labels
        ys = tf.random.categorical(tf.math.log([[0.5, 0.5]]), 2)
        ys = tf.squeeze(ys)
        ys = tf.one_hot(ys, NUM_CLASSES)

        layer = CutMix(probability=1.0, label_smoothing=0.2)
        xs, ys = layer(xs, ys)
        self.assertNotAllClose(ys, 0.0)

    def test_cut_mix_call_results(self):
        xs = tf.cast(
            tf.stack([2 * tf.ones((4, 4, 3)), tf.ones((4, 4, 3))], axis=0,), tf.float32,
        )
        ys = tf.one_hot(tf.constant([0, 1]), 2)

        layer = CutMix(probability=1.0, label_smoothing=0.0)
        xs, ys = layer(xs, ys)

        # At least some pixels should be replaced in the CutMix operation
        self.assertTrue(tf.math.reduce_any(xs[0] == 1.0))
        self.assertTrue(tf.math.reduce_any(xs[0] == 2.0))
        self.assertTrue(tf.math.reduce_any(xs[1] == 1.0))
        self.assertTrue(tf.math.reduce_any(xs[1] == 2.0))
        # No labels should still be close to their original values
        self.assertNotAllClose(ys, 1.0)
        self.assertNotAllClose(ys, 0.0)

    def test_cut_mix_call_results_one_channel(self):
        xs = tf.cast(
            tf.stack([2 * tf.ones((4, 4, 1)), tf.ones((4, 4, 1))], axis=0,), tf.float32,
        )
        ys = tf.one_hot(tf.constant([0, 1]), 2)

        layer = CutMix(probability=1.0, label_smoothing=0.0)
        xs, ys = layer(xs, ys)

        # At least some pixels should be replaced in the CutMix operation
        self.assertTrue(tf.math.reduce_any(xs[0] == 1.0))
        self.assertTrue(tf.math.reduce_any(xs[0] == 2.0))
        self.assertTrue(tf.math.reduce_any(xs[1] == 1.0))
        self.assertTrue(tf.math.reduce_any(xs[1] == 2.0))
        # No labels should still be close to their original values
        self.assertNotAllClose(ys, 1.0)
        self.assertNotAllClose(ys, 0.0)
