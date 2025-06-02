import unittest
import sys, os
from io import StringIO
from contextlib import redirect_stdout

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from stack_machine import StackMachine, parse_module


class TestParseModule(unittest.TestCase):
    def test_basic_parsing_and_loop_map(self):
        module = """
        FUNCTION::: main, []
        ('LOOP',)
        ('ENDLOOP',)
        """
        program, functions, params_map, loop_map = parse_module(module)

        self.assertEqual(loop_map, {0: 1, 1: 0})
        self.assertEqual(functions, {'main': 0})
        self.assertEqual(params_map, {'main': []})

    def test_unmatched_endloop_raises(self):
        module = """
        FUNCTION::: main, []
        ('ENDLOOP',)
        """
        with self.assertRaises(SyntaxError):
            parse_module(module)


class TestStackMachineOps(unittest.TestCase):
    def _run(self, module_text):
        sm = StackMachine()
        sm.load_module(module_text)
        sm.run('main')
        return sm

    def test_const_and_add_int(self):
        module = """
        FUNCTION::: main, []
        ('CONSTI', 2)          
        ('CONSTI', 3)          
        ('ADDI',)
        """
        sm = self._run(module)
        self.assertEqual(sm.stack, [('int', 5)])

    def test_arithmetic_chain_float(self):
        module = """
        FUNCTION::: main, []
        ('CONSTF', 2.5)
        ('CONSTF', 1.5)
        ('ADDF',)
        ('CONSTF', 2.0)
        ('MULF',)
        """
        sm = self._run(module)
        self.assertAlmostEqual(sm.stack[-1][1], 8.0)
        self.assertEqual(sm.stack[-1][0], 'float')


class TestLoopBehavior(unittest.TestCase):
    def test_loop_counter_breaks_at_five(self):
        module = """
        FUNCTION::: main, []
        ('CONSTI', 0)          
        ('LOCAL_SET', 'counter')
        ('LOOP',)
        ('LOCAL_GET', 'counter')
        ('CONSTI', 1)          
        ('ADDI',)
        ('LOCAL_SET', 'counter')
        ('LOCAL_GET', 'counter')
        ('CONSTI', 5)          
        ('LTI',)
        ('CBREAK',)
        ('ENDLOOP',)           
        ('LOCAL_GET', 'counter')
        """
        sm = StackMachine()
        sm.load_module(module)
        sm.run('main')
        self.assertEqual(sm.stack[-1], ('int', 5))

 #
class TestCallRet(unittest.TestCase):
    def test_call_and_ret(self):
        module = """
        FUNCTION::: inc, ['x']
        ('LOCAL_GET', 'x')
        ('CONSTI', 1)          
        ('ADDI',)
        ('RET',)
        FUNCTION::: main, []
        ('CONSTI', 4)          
        ('CALL', 'inc')
        """
        sm = StackMachine()
        sm.load_module(module)
        sm.run('main')
        self.assertEqual(sm.stack, [('int', 5)])


class TestPrint(unittest.TestCase):
    def test_print_outputs_value(self):
        module = """
        FUNCTION::: main, []
        ('CONSTI', 7)          
        ('PRINTI',)
        """
        buf = StringIO()
        with redirect_stdout(buf):
            sm = StackMachine()
            sm.load_module(module)
            sm.run('main')
        self.assertIn("7", buf.getvalue().strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
