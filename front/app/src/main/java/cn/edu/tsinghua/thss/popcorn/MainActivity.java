package cn.edu.tsinghua.thss.popcorn;

import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.Message;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.QRcode.QRcodeActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.ui.AppsFragment;
import cn.edu.tsinghua.thss.popcorn.ui.FragmentAdapter;
import cn.edu.tsinghua.thss.popcorn.ui.MineFragment;
import cn.edu.tsinghua.thss.popcorn.ui.RecordFragment;
import cn.edu.tsinghua.thss.popcorn.ui.ReportFragment;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class MainActivity extends FragmentActivity {
	private ViewPager mPageVp;

	private List<Fragment> mFragmentList = new ArrayList<Fragment>();
	private FragmentAdapter mFragmentAdapter;

	private TextView mTabRecordTv, mTabRepairTv, mTabAppsTv, mTabMineTv,mBodyMeterTv, mBodyRepairTv, mBodyMaintainTv,mbottomTabMeterTv, mbottomTabAppTv;

    private FontAwesomeText mTabRecordFat, mTabRepairFat, mTabAppsFat, mTabMineFat;

    private View mTabRecordLayout, mTabRepairLayout, mTabAppsLayout, mTabMineLayout;
	/**
	 * Tab的那个引导线
	 */
	private ImageView mTabLineIv;
	/**
	 * Fragment
	 */
	private RecordFragment mRecordFg;
	private ReportFragment mReportFg;
    private AppsFragment mAppsFg;
    private MineFragment mMineFg;
	/**
	 * ViewPager的当前选中页
	 */
	private int currentIndex;

	/**
	 * 屏幕的宽度
	 */
	private int screenWidth;

    /**
     * tab 的数量
     */
    private int numOfTabs = 4;

    /**
     * 未完成的任务数量
     */
    private int mRecordUnfinished = 0;
    private int mRepairUnfinished = 0;
    private int mMaintainUnfinished = 0;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
		findById();
		init();
		initTabLineWidth();
        setLocalUsername();
        timer.schedule(task, Config.MAIN_UPDATE_DELAY, Config.MAIN_UPDATE_INTERVAL); // 1s后执行task,经过2s再次执行
	}

    private void setLocalUsername(){
        SharedPreferences sp = getApplicationContext().getSharedPreferences("userInfo", Context.MODE_PRIVATE);
        String username = sp.getString("USERNAME", "");
        Config.DEBUG_USERNAME = username;
    }

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            if (msg.what == 1) {
                //接收消息后要做的处理
                // 增加2个http请求分别用来统计未维修和未保养的数量
                mRecordUnfinished = mRecordFg.unfinished;
                getUnRepairNum();
                getUnMaintainNum();
                // 显示在界面上
                if (mRecordUnfinished > 0 || mRepairUnfinished > 0 || mMaintainUnfinished > 0) {
                    mbottomTabAppTv.setText(String.valueOf(mRecordUnfinished + mRepairUnfinished + mMaintainUnfinished));
                    mbottomTabAppTv.setVisibility(View.VISIBLE);
                    if (mRecordUnfinished > 0) {
                        mbottomTabMeterTv.setText(String.valueOf(mRecordUnfinished));
                        mbottomTabMeterTv.setVisibility(View.VISIBLE);
                        if(mBodyMeterTv == null) {
                            mBodyMeterTv = (TextView)findViewById(R.id.main_body_app_meter_id);
                        }
                        mBodyMeterTv.setText(String.valueOf(mRecordUnfinished));
                        mBodyMeterTv.setVisibility(View.VISIBLE);
                    }
                    else {
                        if(mBodyMeterTv == null) {
                            mBodyMeterTv = (TextView)findViewById(R.id.main_body_app_meter_id);
                        }
                        mbottomTabMeterTv.setVisibility(View.GONE);
                    }
                    if (mRepairUnfinished > 0) {
                        if(mBodyRepairTv == null) {
                            mBodyRepairTv = (TextView)findViewById(R.id.main_body_app_repair_id);
                        }
                        mBodyRepairTv.setText(String.valueOf(mRepairUnfinished));
                        mBodyRepairTv.setVisibility(View.VISIBLE);
                    }
                    else {
                        if(mBodyRepairTv == null) {
                            mBodyRepairTv = (TextView)findViewById(R.id.main_body_app_repair_id);
                        }
                        mBodyRepairTv.setVisibility(View.GONE);
                    }
                    if(mMaintainUnfinished > 0) {
                        if(mBodyMaintainTv == null) {
                            mBodyMaintainTv = (TextView)findViewById(R.id.main_body_app_maintain_id);
                        }
                        mBodyMaintainTv.setText(String.valueOf(mMaintainUnfinished));
                        mBodyMaintainTv.setVisibility(View.VISIBLE);
                    }
                    else {
                        if(mBodyMaintainTv == null) {
                            mBodyMaintainTv = (TextView)findViewById(R.id.main_body_app_maintain_id);
                        }
                        mBodyMaintainTv.setVisibility(View.GONE);
                    }
                } else {
                    mbottomTabMeterTv.setVisibility(View.GONE);
                    mbottomTabAppTv.setVisibility(View.GONE);
                    if(mBodyMeterTv == null) {
                        mBodyMeterTv = (TextView)findViewById(R.id.main_body_app_meter_id);
                    }
                    if(mBodyRepairTv == null) {
                        mBodyRepairTv = (TextView)findViewById(R.id.main_body_app_repair_id);
                    }
                    if(mBodyMaintainTv == null) {
                        mBodyMaintainTv = (TextView)findViewById(R.id.main_body_app_maintain_id);
                    }
                    mBodyMeterTv.setVisibility(View.GONE);
                    mBodyRepairTv.setVisibility(View.GONE);
                    mBodyMaintainTv.setVisibility(View.GONE);
                }
            }
            super.handleMessage(msg);
        };
    };
    Timer timer = new Timer();
    TimerTask task = new TimerTask() {

        @Override
        public void run() {
            // 需要做的事:发送消息
            Message message = new Message();
            message.what = 1;
            handler.sendMessage(message);
        }
    };

	private void findById() {
		mTabRecordTv = (TextView) this.findViewById(R.id.id_record_tv);
        mTabRepairTv = (TextView) this.findViewById(R.id.id_repair_tv);
        mTabAppsTv = (TextView) this.findViewById(R.id.id_apps_tv);
        mTabMineTv = (TextView) this.findViewById(R.id.id_mine_tv);

        mTabRecordFat = (FontAwesomeText) findViewById(R.id.id_record_fat);
        mTabRepairFat = (FontAwesomeText) findViewById(R.id.id_repair_fat);
        mTabAppsFat = (FontAwesomeText) findViewById(R.id.id_apps_fat);
        mTabMineFat = (FontAwesomeText) findViewById(R.id.id_mine_fat);

        mTabRecordLayout = this.findViewById(R.id.id_tab_record_ll);
        mTabRepairLayout = this.findViewById(R.id.id_tab_repair_ll);
        mTabAppsLayout = this.findViewById(R.id.id_tab_apps_ll);
        mTabMineLayout = this.findViewById(R.id.id_tab_mine_ll);

        mbottomTabMeterTv = (TextView)this.findViewById(R.id.main_bottom_tab_meter_id);
        mbottomTabAppTv = (TextView)this.findViewById(R.id.main_bottom_tab_app_id);
        mBodyMeterTv = (TextView)this.findViewById(R.id.main_body_app_meter_id);
        mBodyRepairTv = (TextView)this.findViewById(R.id.main_body_app_repair_id);
        mBodyMaintainTv = (TextView)this.findViewById(R.id.main_body_app_maintain_id);

		mTabLineIv = (ImageView) this.findViewById(R.id.id_tab_line_iv);
		mPageVp = (ViewPager) this.findViewById(R.id.id_page_vp);
	}

	private void init() {
        mAppsFg = new AppsFragment();
		mRecordFg = new RecordFragment();
		mReportFg = new ReportFragment();
        mMineFg = new MineFragment();

        mFragmentList.add(mAppsFg);
		mFragmentList.add(mRecordFg);
		mFragmentList.add(mReportFg);
        mFragmentList.add(mMineFg);
        if (mFragmentAdapter == null) {
            mFragmentAdapter = new FragmentAdapter(this.getSupportFragmentManager(), mFragmentList);
        } else {
            mFragmentAdapter.setFragmentsList(getSupportFragmentManager(),mFragmentList);
        }
		mPageVp.setAdapter(mFragmentAdapter);
		mPageVp.setCurrentItem(0);

        mTabAppsLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(0, false);
            }
        });

        mTabRecordLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(1, false);
            }
        });

        mTabRepairLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(2, false);
            }
        });

        mTabMineLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(3, false);
            }
        });

		mPageVp.setOnPageChangeListener(new OnPageChangeListener() {

			/**
			 * state滑动中的状态 有三种状态（0，1，2） 1：正在滑动 2：滑动完毕 0：什么都没做。
			 */
			@Override
			public void onPageScrollStateChanged(int state) {
                // code goes here
			}

			/**
			 * position :当前页面，及你点击滑动的页面 offset:当前页面偏移的百分比
			 * offsetPixels:当前页面偏移的像素位置
             * This method will be invoked when the current page is scrolled
			 */
			@Override
			public void onPageScrolled(int position, float offset,
					int offsetPixels) {
				LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) mTabLineIv
						.getLayoutParams();

				//Log.e("offset:", offset + "");
				/**
				 * 利用currentIndex(当前所在页面)和position(下一个页面)以及offset来
				 * 设置mTabLineIv的左边距 滑动场景：
				 * 记4个页面,
				 * 从左到右分别为0,1,2, 3
				 */

				if (currentIndex == 0 && position == 0)// 0->1
				{
					lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));

				} else if (currentIndex == 1 && position == 0) // 1->0
				{
					lp.leftMargin = (int) (-(1 - offset)
							* (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));

				} else if (currentIndex == 1 && position == 1) // 1->2
				{
					lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));
				} else if (currentIndex == 2 && position == 1) // 2->1
				{
					lp.leftMargin = (int) (-(1 - offset)
							* (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));
				} else if (currentIndex == 2 && position == 2) // 2->3
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                } else if (currentIndex == 3 && position == 2) // 3->2
                {
                    lp.leftMargin = (int) (-(1 - offset)
                            * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                }else if (currentIndex == 3 && position == 3) // 3->3
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                }
                mTabLineIv.setLayoutParams(lp);
			}


            // This method will be invoked when a new page becomes selected.
			@Override
			public void onPageSelected(int position) {
				resetTabColor();
				switch (position) {
                    case 0:
                        mTabAppsTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabAppsFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 1:

                        mTabRecordTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabRecordFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 2:
                        mTabRepairTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabRepairFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 3:
                        mTabMineTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabMineFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
				}
				currentIndex = position;
			}
		});

	}

	/**
	 * 设置滑动条的宽度为屏幕的1/4(根据Tab的个数而定)
	 */
	private void initTabLineWidth() {
		DisplayMetrics dpMetrics = new DisplayMetrics();
		getWindow().getWindowManager().getDefaultDisplay()
				.getMetrics(dpMetrics);
		screenWidth = dpMetrics.widthPixels;
		LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) mTabLineIv
				.getLayoutParams();
		lp.width = screenWidth / numOfTabs;
		mTabLineIv.setLayoutParams(lp);
	}

	/**
	 * 重置导航栏的颜色
	 */
	private void resetTabColor() {
		mTabRecordTv.setTextColor(Color.parseColor("#D3D3D3"));
		mTabRepairTv.setTextColor(Color.parseColor("#D3D3D3"));
        mTabAppsTv.setTextColor(Color.parseColor("#D3D3D3"));
        mTabMineTv.setTextColor(Color.parseColor("#D3D3D3"));

        mTabRecordFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabRepairFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabAppsFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabMineFat.setTextColor(Color.parseColor("#D3D3D3"));
	}


    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && event.getRepeatCount() == 0) {
            Intent intent = new Intent(Intent.ACTION_MAIN);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);// 注意
            intent.addCategory(Intent.CATEGORY_HOME);
            this.startActivity(intent);
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        switch (item.getItemId()){
            case R.id.scan_btn:
                try {
                    Intent intent = new Intent(this, QRcodeActivity.class);
                    Bundle bundle = new Bundle();
                    intent.putExtras(bundle);
                    startActivity(intent);
                }
                catch (Exception e){
                    Log.e("Exception", e.getMessage(), e);
                }
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    private void getUnRepairNum(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.REPAIR_TASK_LIST_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try{
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if(status.equals("ok")) {
                                JSONArray repairTaskList = jsonObject.getJSONArray("data");
                                mRepairUnfinished = repairTaskList.length();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "服务器内部出错", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    private void getUnMaintainNum(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.MAINTAIN_TASK_LIST_URL,
                params,
                new RequestCallBack<String>() {
                    @Override
                    public void onStart() {
                    }
                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }
                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if (status.equals("ok")) {
                                JSONArray maintainTaskList = jsonObject.getJSONArray("data");
                                mMaintainUnfinished = maintainTaskList.length();
                            } else {
                                Toast.makeText(getApplicationContext(), "服务器内部出错", Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    public void onDestroy(){
        super.onDestroy();
        timer.cancel();
    }
}
