add_dependencies({
    muting: 'js/muting',
    stream_data: 'js/stream_data',
    stream_sort: 'js/stream_sort',
    unread: 'js/unread',
});

set_global('blueslip', {});

var tg = require('js/topic_generator.js');

function is_even(i) { return i % 2 === 0; }
function is_odd(i) { return i % 2 === 1; }

(function test_basics() {
    var gen = tg.list_generator([10, 20, 30]);
    assert.equal(gen.next(), 10);
    assert.equal(gen.next(), 20);
    assert.equal(gen.next(), 30);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    var gen1 = tg.list_generator([100, 200]);
    var gen2 = tg.list_generator([300, 400]);
    var outers = [gen1, gen2];
    gen = tg.chain(outers);
    assert.equal(gen.next(), 100);
    assert.equal(gen.next(), 200);
    assert.equal(gen.next(), 300);
    assert.equal(gen.next(), 400);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    gen = tg.wrap([5, 15, 25, 35], 25);
    assert.equal(gen.next(), 25);
    assert.equal(gen.next(), 35);
    assert.equal(gen.next(), 5);
    assert.equal(gen.next(), 15);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    gen = tg.wrap_exclude([5, 15, 25, 35], 25);
    assert.equal(gen.next(), 35);
    assert.equal(gen.next(), 5);
    assert.equal(gen.next(), 15);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    gen = tg.wrap([5, 15, 25, 35], undefined);
    assert.equal(gen.next(), 5);

    gen = tg.wrap_exclude([5, 15, 25, 35], undefined);
    assert.equal(gen.next(), 5);

    gen = tg.wrap([5, 15, 25, 35], 17);
    assert.equal(gen.next(), 5);

    gen = tg.wrap([], 42);
    assert.equal(gen.next(), undefined);

    var ints = tg.list_generator([1, 2, 3, 4, 5]);
    gen = tg.filter(ints, is_even);
    assert.equal(gen.next(), 2);
    assert.equal(gen.next(), 4);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    ints = tg.list_generator([]);
    gen = tg.filter(ints, is_even);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    ints = tg.list_generator([10, 20, 30]);

    function mult10(x) { return x * 10; }

    gen = tg.map(ints, mult10);
    assert.equal(gen.next(), 100);
    assert.equal(gen.next(), 200);
}());

(function test_fchain() {
    var mults = function (n) {
        var ret = 0;
        return {
            next: function () {
                ret += n;
                return (ret <= 100) ? ret : undefined;
            },
        };
    };

    var ints = tg.list_generator([29, 43]);
    var gen = tg.fchain(ints, mults);
    assert.equal(gen.next(), 29);
    assert.equal(gen.next(), 58);
    assert.equal(gen.next(), 87);
    assert.equal(gen.next(), 43);
    assert.equal(gen.next(), 86);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    ints = tg.wrap([33, 34, 37], 37);
    ints = tg.filter(ints, is_odd);
    gen = tg.fchain(ints, mults);
    assert.equal(gen.next(), 37);
    assert.equal(gen.next(), 74);
    assert.equal(gen.next(), 33);
    assert.equal(gen.next(), 66);
    assert.equal(gen.next(), 99);
    assert.equal(gen.next(), undefined);
    assert.equal(gen.next(), undefined);

    var undef = function () {
        return undefined;
    };

    global.blueslip.error = function (msg) {
        assert.equal(msg, 'Invalid generator returned.');
    };

    ints = tg.list_generator([29, 43]);
    gen = tg.fchain(ints, undef);
    gen.next();
}());


(function test_topics() {
    var streams = [1, 2, 3, 4];
    var topics = {};

    topics[1] = ['read', 'read', '1a', '1b', 'read', '1c'];
    topics[2] = [];
    topics[3] = ['3a', 'read', 'read', '3b', 'read'];
    topics[4] = ['4a'];

    function has_unread_messages(stream, topic) {
        return topic !== 'read';
    }

    function get_topics(stream) {
        return topics[stream];
    }

    function next_topic(curr_stream, curr_topic) {
        return tg.next_topic(
            streams,
            get_topics,
            has_unread_messages,
            curr_stream,
            curr_topic);
    }

    assert.deepEqual(next_topic(1, '1a'),
                     {stream: 1, topic: '1b'});
    assert.deepEqual(next_topic(1, undefined),
                     {stream: 1, topic: '1a'});
    assert.deepEqual(next_topic(2, 'bogus'),
                     {stream: 3, topic: '3a'});
    assert.deepEqual(next_topic(3, '3b'),
                     {stream: 3, topic: '3a'});
    assert.deepEqual(next_topic(4, '4a'),
                     {stream: 1, topic: '1a'});
    assert.deepEqual(next_topic(undefined, undefined),
                     {stream: 1, topic: '1a'});


    // Now test the deeper function that is wired up to
    // real functions stream_data/stream_sort/unread.
    var curr_stream = 'announce';
    var curr_topic = 'whatever';

    global.stream_sort.get_streams = function () {
        return ['announce', 'muted', 'devel', 'test here'];
    };

    global.stream_data.get_recent_topics = function (stream) {
        if (stream === 'muted') {
            return [
                {subject: 'red herring'},
            ];
        }
        if (stream === 'devel') {
            return [
                {subject: 'muted'},
                {subject: 'python'},
            ];
        }
    };

    var devel_stream_id = 555;

    global.stream_data.get_stream_id = function (stream_name) {
        if (stream_name === 'devel') {
            return devel_stream_id;
        }

        return 999;
    };

    global.stream_data.name_in_home_view = function (stream_name) {
        return (stream_name !== 'muted');
    };

    global.unread.topic_has_any_unread = function (stream_id) {
        return (stream_id === devel_stream_id);
    };

    global.muting.is_topic_muted = function (stream_name, topic) {
        return (topic === 'muted');
    };

    var next_item = tg.get_next_topic(curr_stream, curr_topic);
    assert.deepEqual(next_item, {
        stream: 'devel',
        topic: 'python',
    });
}());
