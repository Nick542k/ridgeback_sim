from setuptools import setup

package_name = 'ridgeback_sim_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Nithish',
    author_email='nithish@todo.todo',
    maintainer='Nithish',
    maintainer_email='nithish@todo.todo',
    description='Python control nodes for Ridgeback AMR simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'velocity_commander = ridgeback_sim_control.velocity_commander:main',
            'sensor_listener = ridgeback_sim_control.sensor_listener:main',
            'obstacle_avoider = ridgeback_sim_control.obstacle_avoider:main',
            'autonomous_navigator = ridgeback_sim_control.autonomous_navigator:main',
        ],
    },
)
